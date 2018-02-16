#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import sys
import os
import shutil
import glob
import numpy as np

# Parse the inputs
simulation_dir = sys.argv[1]
r_max = float(sys.argv[2])
thin_factor = int(sys.argv[3])

print simulation_dir
print r_max
print thin_factor # If we don't want to get data from every time point...

# create a new 'OpenFOAMReader'
vtk_folder = simulation_dir + 'VTK/'
patches_folder = vtk_folder + 'allPatches/'
patch_paths = glob.glob(patches_folder + '*.vtk')
patch_file_names = [os.path.basename(z) for z in patch_paths]

# Sort the files for my sanity, may not actually be necessary
patch_file_names = np.array(patch_file_names)
file_numbers_str = [z.replace('_','.').split('.')[1] for z in patch_file_names]
file_numbers= np.array(file_numbers_str).astype(np.int)

order = np.argsort(file_numbers)

patch_paths = np.array(patch_paths)
patch_paths = patch_paths[order]
# Now thin the results
patch_paths = patch_paths[::thin_factor]
print patch_paths

simulation = LegacyVTKReader(FileNames=patch_paths)

# From the patches (cell data), create point data
simulation = CellDatatoPointData(Input=simulation)

# create a new 'Slice'
slice1 = Slice(Input=simulation)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [r_max/2., 0.0, 0.5]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

# set active source
SetActiveSource(slice1)

# create a new 'Calculator'
calculator1 = Calculator(Input=slice1)

# Properties modified on calculator1
pi_str = str(np.pi)
calculator1.Function = '2*' + pi_str + '*coordsX*c'
calculator1.ResultArrayName = '2p_r_c'

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(Input=calculator1)

folder_path = sys.argv[1] + '/total_solute/'
if os.path.isdir(folder_path):
    shutil.rmtree(folder_path)
os.makedirs(folder_path)

SaveData(folder_path + 'total_solute.csv', proxy=integrateVariables1, WriteAllTimeSteps=1)

# Write what the thin factor was to disk...we need this later to get what the *actual*
# times are!
with open(folder_path + 'thin_factor.txt', 'wb') as fi:
    fi.write(str(thin_factor))