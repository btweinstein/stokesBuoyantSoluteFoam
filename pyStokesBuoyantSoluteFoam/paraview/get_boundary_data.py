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

print simulation_dir
print r_max

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

line_points = []
axis_names = []

line_tolerance = 3e-16

### Left Axis ###
axis_names.append('axis_left')

left_line_points = [
    [0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0]
]
line_points.append(left_line_points)

### Top Axis ###
axis_names.append('axis_top')

top_line_points = [
    [0.0, 0.0, 1.0],
    [r_max, 0.0, 1.0]
]
line_points.append(top_line_points)

### Bottom Axis ###
axis_names.append('axis_bottom')

bottom_line_points = [
    [0.0, 0.0, 0.0],
    [r_max, 0.0, 0.0]
]
line_points.append(top_line_points)

for cur_line_points, cur_axis_name in zip(line_points, axis_names):
    cur_line = PlotOverLine(Input=slice1, Source='High Resolution Line Source')

    cur_line.Source.Point1 = cur_line_points[0]
    cur_line.Source.Point2 = cur_line_points[1]

    # Properties modified on plotOverLine1
    cur_line.Tolerance = 3e-16

    # save data
    folder_path = sys.argv[1] + '/' + cur_axis_name + '/'
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

    SaveData(folder_path + cur_axis_name + '.csv', proxy=cur_line, WriteAllTimeSteps=1)