import pint # For easy units
import subprocess
import numpy as np
import os

# Get path to *this* file. Necessary when applying gmsh to the packaged geometry
full_path = os.path.realpath(__file__)
file_dir = os.path.dirname(full_path)
parent_dir = os.path.dirname(file_dir)

# Define constants

ureg = pint.UnitRegistry()

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


class Simulation(object):
    def __init__(self, V=None, mu=None, r_yeast=None):
        self.V = V  # Volume: must have units

        self.mu = mu  # Viscosity: must have units
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
        self.nd_r_yeast = (r_yeast / self.Lc).to_base_units()

        # Calculate the dimensionless length of the petri dish
        self.nd_r_petri = (r_petri / self.Lc).to_base_units()

    def create_gmsh(self, mesh_name, mesh_size=0.1, slice_angle=2.5):
        lc = mesh_size
        r_yeast = self.nd_r_yeast.magnitude
        r_petri = self.nd_r_petri.magnitude

        subprocess.call(['gmsh', '-1', '-2', '-3',
                         '-setnumber', 'lc', str(lc),
                         '-setnumber', 'r_yeast', str(r_yeast),
                         '-setnumber', 'r_petri', str(r_petri),
                         '-setnumber', 'slice_angle', str(slice_angle),
                         file_dir + '/yeast_radially_symmetric.geo',
                         '-o', str(mesh_name)]
                        )