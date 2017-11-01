#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import sys
import os
import shutil

# create a new 'OpenFOAMReader'
simulation = OpenFOAMReader(FileName=sys.argv[1])

# Properties modified on j_m_colony_sweep_0p10foam
simulation.MeshRegions = ['internalMesh', 'yeast_top', 'yeast_bottom', 'petri_top', 'petri_outer', 'petri_bottom']
simulation.CellArrays = ['U', 'c', 'p', 'p_rgh']

# create a new 'Slice'
slice1 = Slice(Input=simulation)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [1.99952399730682, 0.0, 0.5]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [1.99952399730682, 0.0, 0.5]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]


# set active source
SetActiveSource(slice1)

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=slice1, Source='High Resolution Line Source')

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point2 = [0.0, 0.0, 1.0]

# Properties modified on plotOverLine1
plotOverLine1.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point2 = [0.0, 0.0, 1.0]

# save data
folder_path = sys.argv[1] + '/left_axis_csv/'
if os.path.isdir(folder_path):
    shutil.rmtree(folder_path)
os.makedirs(folder_path)

SaveData(folder_path + 'left_axis.csv', proxy=plotOverLine1, WriteAllTimeSteps=1)