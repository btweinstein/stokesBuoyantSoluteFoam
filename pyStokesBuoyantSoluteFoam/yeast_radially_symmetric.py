import pint # For easy units
import subprocess
import numpy as np
import os
import shutil
import cPickle as pkl
import glob
import pandas as pd

import PyFoam
from PyFoam.RunDictionary.SolutionFile import SolutionFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.BoundaryDict import BoundaryDict


# Get path to *this* file. Necessary when applying gmsh to the packaged geometry
full_path = os.path.realpath(__file__)
file_dir = os.path.dirname(full_path)
parent_dir = os.path.dirname(file_dir)

sim_setup_dir = file_dir + '/simulation_setups/yeast_radially_symmetric/'
paraview_script_dir = file_dir + '/paraview/'

# Define constants

from . import ureg # Use the package unit registry...

D = 2.5e-6 * (ureg.cm**2 / ureg.sec)
r_petri = 8.7/2. * (ureg.cm) # cm
g = 9.80665 * (ureg.meter/ureg.second**2)  # meter/second^2

mu_dict = {}
mu_dict[2.2] = 30 * ureg.pascal * ureg.second
mu_dict[2.5] = 50 * ureg.pascal * ureg.second

rho_0 = 1.0167 * ureg.gram / ureg.milliliter
rho_f = 1.0077 * ureg.gram / ureg.milliliter

delta_rho = rho_0 - rho_f

beta = delta_rho /rho_f # Has units...but dimensionless when multiplied by c, which is what we use it for.

# The tricky parameter to fit: the mass flux per yeast cell! It should be on the
# order of, from my estimates, 2.5 pg/(um^2/hour). It *may* depend on if the yeast
# is covered or not with the fluid, so I'm going to keep it as an input parameter.
# The other parameters are relatively independent of exactly what we change.
# With that said, there are a couple of constants we can hand-wavily define for my use.

rho_yeast = 1.1029 * ureg.g/ureg.mL # From the yeast size measurement paper

r_single_yeast = 2.5 * ureg.um # From the yeast size measurement paper

t_yeast = 90*ureg.minute # Yeast generation time estimation while fermenting

A_single_yeast_projection = (np.pi*r_single_yeast**2).to(ureg.um**2)

V_single_yeast = ((4./3.)*np.pi*r_single_yeast**3).to(ureg.um**3)

m_single_yeast = (rho_yeast * V_single_yeast).to(ureg.pg)

# Therefore, our best estimate of the mass flux is...
j_m_single_yeast = (m_single_yeast / (A_single_yeast_projection * t_yeast)).to(ureg.pg/(ureg.hour * ureg.um**2))

# Defining the boundary condition for sucking up nutrients...
nutrient_absorbing_bc = {'fractionExpression': '"0"',
                         'gradientExpression': '"-G*c"',
                         'type': 'groovyBC',
                         'value': 'uniform 1.0',
                         'variables': '$swakVariables'}

class Simulation(object):
    def __init__(self, V=None, mu=None, r_yeast=None, j_m_colony=None, sim_path=None,
                 yeast_position=None, covered_interface=None):
        self.V = V  # Volume: must have units
        self.mu = mu # Viscosity: must have units
        self.r_yeast = r_yeast # Physical radius of yeast colony
        self.j_m_colony = j_m_colony # Mass flux per unit area of yeast
        self.sim_path = sim_path
        self.sim_basename = os.path.basename(sim_path)

        self.nu = (self.mu / rho_0)
        self.nu.ito(ureg.centimeter ** 2 / ureg.second)

        self.h = self.V / (np.pi * r_petri ** 2)
        self.h.ito(ureg.mm)

        # Calculate Ra_star
        self.Ra_star = (self.h ** 3) * g * beta / (D * self.nu)
        self.Ra_star.ito_base_units()

        # Set the characteristic length and time scale
        self.Lc = self.h
        self.Tc = (self.h ** 2 / D).to(ureg.day)

        # Calculate the dimensionless length of the yeast
        self.nd_r_yeast = (self.r_yeast / self.Lc).to_base_units()

        # Calculate the dimensionless length of the petri dish
        self.nd_r_petri = (r_petri / self.Lc).to_base_units()

        # Get G based on the input parameters
        self.G = (self.h*self.j_m_colony)/(D*rho_0*beta)
        self.G.ito(ureg.dimensionless)

        self.openfoam_case = None
        self.covered_interface = covered_interface
        self.yeast_position = yeast_position

        self.cur_process = None # The actual process that the class is running outside of python.

    @classmethod
    def load(cls, pkl_path):
        with open(pkl_path, 'rb') as fi:
            return pkl.load(fi)

    def create_gmsh(self, mesh_size=0.1, slice_angle=2.5, **kwargs):

        lc = mesh_size
        r_yeast = self.nd_r_yeast.magnitude
        r_petri = self.nd_r_petri.magnitude

        geo_path = sim_setup_dir + '/yeast_radially_symmetric.geo'
        final_mesh_path = self.sim_path + '/' + self.sim_basename + '.msh'

        subprocess.call(['gmsh', '-1', '-2', '-3',
                         '-setnumber', 'lc', str(lc),
                         '-setnumber', 'r_yeast', str(r_yeast),
                         '-setnumber', 'r_petri', str(r_petri),
                         '-setnumber', 'slice_angle', str(slice_angle),
                         geo_path, '-o', final_mesh_path]
                        )
        # Now convert to openfoam format
        subprocess.call(['gmshToFoam', final_mesh_path,
                         '-case', self.sim_path])

    def create_openfoam_sim(self, overwrite_old_sim=False, **kwargs):
        # yeast_position: whether the yeast is on the TOP or BOTTOM of the geometry.
        # covered_interface: whether the free interface is covered or not.

        # Copy the skeleton into the new location. If the location already exists, delete & replace.
        continue_sim = True

        if os.path.isdir(self.sim_path): # If the simulation already exists
            if not overwrite_old_sim:
                print r'The simulation already exists...I\'m not going to delete it'
                continue_sim = False
            else:
                shutil.rmtree(self.sim_path)
        if continue_sim:

            shutil.copytree(sim_setup_dir, self.sim_path)
            shutil.copy(self.sim_path + '/yeast_radially_symmetric.foam', self.sim_path + '/' + self.sim_basename + '.foam')

            self.create_gmsh(**kwargs)

            self.openfoam_case = SolutionDirectory(self.sim_path)

            # Update the parameters file to match the desired parameters
            parameters = ParsedParameterFile(self.sim_path + '/parameters', treatBinaryAsASCII=True)
            parameters['Ra'] = self.Ra_star.magnitude
            parameters['swakVariables'] = [r'"G=' + str(self.G.magnitude) + r';"']
            parameters.writeFile()

            # Update the boundary file and conditions as appropriate...
            # Remember, the only things that vary are whether the interface is covered
            # and the location of the yeast.
            boundary_dict = BoundaryDict(self.sim_path, treatBinaryAsASCII=True)
            U_dict = ParsedParameterFile(self.openfoam_case.initialDir() + '/U', treatBinaryAsASCII=True)
            c_dict = ParsedParameterFile(self.openfoam_case.initialDir() + '/c', treatBinaryAsASCII=True)


            # The below definitions are *always* true, regardless of what I vary.
            boundary_dict['left_sym']['type'] = 'wedge'
            boundary_dict['right_sym']['type'] = 'wedge'

            boundary_dict['yeast_bottom']['type'] = 'wall'
            boundary_dict['petri_outer']['type'] = 'wall'
            boundary_dict['petri_bottom']['type'] = 'wall'

            ### COVERED INTERFACE ###
            if self.covered_interface is True: # The top is a wall regardless of where the yeast is
                # Update mesh boundary info...
                boundary_dict['petri_top']['type'] = 'wall'
                boundary_dict['yeast_top']['type'] = 'wall'

                # Update velocty fields...
                U_dict['boundaryField']['petri_top']['type'] = 'noSlip'
                U_dict['boundaryField']['yeast_top']['type'] = 'noSlip'

                # Update concentration fields...
                if self.yeast_position is 'top':
                    c_dict['boundaryField']['yeast_top'] = nutrient_absorbing_bc
                    c_dict['boundaryField']['yeast_bottom'] = {'type': 'zeroGradient'}

                elif self.yeast_position is 'bottom':
                    c_dict['boundaryField']['yeast_bottom'] = nutrient_absorbing_bc
                    c_dict['boundaryField']['yeast_top'] = {'type': 'zeroGradient'}

                else:
                    print 'Please define the yeast position...'

            ### FREE INTERFACE ###
            elif self.covered_interface is False: # The interface is free...things change depending on where yeast is
                boundary_dict['petri_top']['type'] = 'patch' # Always slip
                U_dict['boundaryField']['petri_top']['type']= 'slip'

                if self.yeast_position is 'top':
                    boundary_dict['yeast_top']['type'] = 'wall'
                    U_dict['boundaryField']['yeast_top']['type'] = 'noSlip'

                    c_dict['boundaryField']['yeast_top'] = nutrient_absorbing_bc
                    c_dict['boundaryField']['yeast_bottom'] = {'type': 'zeroGradient'}

                elif self.yeast_position is 'bottom':
                    boundary_dict['yeast_top']['type'] = 'patch'
                    U_dict['boundaryField']['yeast_top']['type'] = 'slip'

                    c_dict['boundaryField']['yeast_top'] = {'type': 'zeroGradient'}
                    c_dict['boundaryField']['yeast_bottom'] = nutrient_absorbing_bc

                else:
                    print 'Please define the yeast position...'

            else:
                print 'Please specify whether the interface is covered (true) or not (false)...'

            boundary_dict.writeFile()
            U_dict.writeFile()
            c_dict.writeFile()

            # Pickle this class so that we know what precise parameters were used.
            with open(self.sim_path + '/' + self.sim_basename +'.pkl', 'wb') as fi:
                pkl.dump(self, fi)

    def run_simulation(self):
        # Open a file for the log file
        with open(self.sim_path + '/log.txt', 'wb') as f_out, \
                open(self.sim_path + '/err.txt', 'wb') as f_err:
            self.cur_process = subprocess.Popen(['stokesBuoyantSoluteFoam', '-case', self.sim_path],
                                                stdout=f_out, stderr=f_err)

    def get_physical_t(self, t_non_dim):
        return (self.Tc*t_non_dim).to(ureg.hour)

    def get_physical_v(self, v_non_dim):
        vc = D/self.h
        return (vc*v_non_dim).to(ureg.mm/ureg.day)

    def get_wall_shear_stress(self):
        with open(self.sim_path + '/wall_shear_stress_log.txt', 'wb') as f_out, \
                open(self.sim_path + '/wall_shear_stress_err.txt', 'wb') as f_err:
            self.cur_process = subprocess.Popen(['stokesBuoyantSoluteFoam', '-case', self.sim_path,
                                                 '-postProcess', '-func', 'wallShearStress'],
                                                stdout=f_out, stderr=f_err)

    def paraview_extract_boundary_info(self):
        script_path = paraview_script_dir + 'get_boundary_data.py'
        rmax = self.nd_r_petri.magnitude
        with open(self.sim_path + '/boundary_log.txt', 'wb') as f_out, \
                open(self.sim_path + '/boundary_err.txt', 'wb') as f_err:
            self.cur_process = subprocess.Popen(['pvbatch', script_path, self.sim_path + '/', str(rmax)],
                                                stdout=f_out, stderr=f_err)

    def get_boundary_info_df(self, desired_axis):
        # Requires paraview_extract_boundary_info to be run first!

        csv_files = glob.glob(self.sim_path + '/axis_' + desired_axis + '/*')
        if len(csv_files) == 0:
            print 'I can\'t find info on that axis...'
            raise ValueError

        time_list = [] # Organize all of the time points

        contents = glob.glob(self.sim_path + '/*')
        for cur_folder in contents:
            cur_basename = os.path.basename(cur_folder)
            time = None
            try:
                time = float(cur_basename)
                time_list.append(time)
            except ValueError:
                pass
        time_list.sort()

        df_list = []
        for cur_csv in csv_files:
            cur_df = pd.read_csv(cur_csv)
            cur_df.rename(columns={'U:0': 'ux', 'U:1': 'uy', 'U:2': 'uz',
                                   'wallShearStress:0': 'tau_nx', 'wallShearStress:1': 'tau_ny',
                                   'wallShearStress:2': 'tau_nz',
                                   'Points:0': 'x', 'Points:1': 'y', 'Points:2': 'z'}, inplace=True)
            # Figure out what timepoint this corresponds to
            csv_basename = os.path.basename(cur_csv)

            time_index = int(csv_basename.split('.')[1])
            time = time_list[time_index]

            cur_df['time_index'] = time_index
            cur_df['time'] = time

            df_list.append(cur_df)

        df = pd.concat(df_list)
        return df
