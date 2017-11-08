#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import sys
import os
import shutil

# Parse the inputs
simulation_dir = sys.argv[1]
r_max = float(sys.argv[2])

print simulation_dir
print r_max

# create a new 'OpenFOAMReader'
simulation = OpenFOAMReader(FileName=simulation_dir)

# Properties modified on j_m_colony_sweep_0p10foam
simulation.MeshRegions = ['yeast_top', 'yeast_bottom', 'petri_top', 'petri_outer', 'petri_bottom', 'internalMesh']
simulation.CellArrays = ['U', 'c', 'p', 'p_rgh', 'wallShearStress']

simulation.MeshParts = ['internalMesh', 'yeast_top - patch', 'yeast_bottom - patch',
                        'petri_top - patch', 'petri_outer - patch',
                        'petri_bottom - patch']
simulation.VolumeFields = ['U', 'c', 'p', 'p_rgh', 'wallShearStress']

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