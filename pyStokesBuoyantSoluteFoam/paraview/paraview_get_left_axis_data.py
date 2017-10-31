#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import sys
import os
import shutil

# create a new 'OpenFOAMReader'
simulation = OpenFOAMReader(FileName=sys.argv[1])

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on j_m_colony_sweep_0p10foam
simulation.MeshRegions = ['internalMesh', 'yeast_top', 'yeast_bottom', 'petri_top', 'petri_outer', 'petri_bottom']
simulation.CellArrays = ['U', 'c', 'p', 'p_rgh']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1234, 791]

# show data in view
simulation_display = Show(simulation, renderView1)
# trace defaults for the display properties.
simulation_display.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
#simulation_display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# reset view to fit data
renderView1.ResetCamera()

# create a new 'Slice'
slice1 = Slice(Input=simulation)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [1.99952399730682, 0.0, 0.5]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [1.99952399730682, 0.0, 0.5]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

# show data in view
slice1Display = Show(slice1, renderView1)
# trace defaults for the display properties.
slice1Display.Representation = 'Surface'

# hide data in view
#Hide(simulation, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(slice1Display, ('CELLS', 'c'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'c'
cLUT = GetColorTransferFunction('c')

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# get color legend/bar for cLUT in view renderView1
cLUTColorBar = GetScalarBar(cLUT, renderView1)

# change scalar bar placement
cLUTColorBar.Position = [0.2662398703403566, 0.7637168141592922]
cLUTColorBar.ScalarBarLength = 0.33

# set active source
SetActiveSource(simulation)

# set active source
SetActiveSource(slice1)

animationScene1.Play()

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# set scalar coloring
ColorBy(slice1Display, ('CELLS', 'U', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(cLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')

# get color legend/bar for uLUT in view renderView1
uLUTColorBar = GetScalarBar(uLUT, renderView1)

# change scalar bar placement
uLUTColorBar.Orientation = 'Horizontal'
uLUTColorBar.Position = [0.345656401944895, 0.6828065739570167]
uLUTColorBar.ScalarBarLength = 0.3299999999999993

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=slice1,
    Source='High Resolution Line Source')

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point2 = [0.0, 0.0, 1.0]

# Properties modified on plotOverLine1
plotOverLine1.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point2 = [0.0, 0.0, 1.0]

# show data in view
plotOverLine1Display = Show(plotOverLine1, renderView1)
# trace defaults for the display properties.
plotOverLine1Display.Representation = 'Surface'

# Create a new 'Line Chart View'
lineChartView1 = CreateView('XYChartView')
lineChartView1.ViewSize = [612, 791]

# get layout
layout1 = GetLayout()

# place view in the layout
layout1.AssignView(2, lineChartView1)

# show data in view
plotOverLine1Display_1 = Show(plotOverLine1, lineChartView1)

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
lineChartView1.Update()

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesVisibility = ['c', 'p', 'p_rgh', 'U_Z', 'U_Magnitude']
plotOverLine1Display_1.SeriesColor = ['arc_length', '0', '0', '0', 'c', '0.889998', '0.100008', '0.110002', 'p', '0.220005', '0.489998', '0.719997', 'p_rgh', '0.300008', '0.689998', '0.289998', 'U_X', '0.6', '0.310002', '0.639994', 'U_Y', '1', '0.500008', '0', 'U_Z', '0.650004', '0.340002', '0.160006', 'U_Magnitude', '0', '0', '0', 'vtkValidPointMask', '0.889998', '0.100008', '0.110002', 'Points_X', '0.220005', '0.489998', '0.719997', 'Points_Y', '0.300008', '0.689998', '0.289998', 'Points_Z', '0.6', '0.310002', '0.639994', 'Points_Magnitude', '1', '0.500008', '0']
plotOverLine1Display_1.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'c', '0', 'p', '0', 'p_rgh', '0', 'vtkValidPointMask', '0']
plotOverLine1Display_1.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'c', '1', 'p', '1', 'p_rgh', '1', 'vtkValidPointMask', '1']
plotOverLine1Display_1.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'c', '2', 'p', '2', 'p_rgh', '2', 'vtkValidPointMask', '2']
plotOverLine1Display_1.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'c', '0', 'p', '0', 'p_rgh', '0', 'vtkValidPointMask', '0']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesVisibility = ['c', 'p', 'p_rgh', 'U_Y', 'U_Z', 'U_Magnitude']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesVisibility = ['c', 'p', 'p_rgh', 'U_X', 'U_Y', 'U_Z', 'U_Magnitude']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesVisibility = ['arc_length', 'c', 'p', 'p_rgh', 'U_X', 'U_Y', 'U_Z', 'U_Magnitude']

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesVisibility = ['c', 'p', 'p_rgh', 'U_X', 'U_Y', 'U_Z', 'U_Magnitude']

# save data
folder_path = sys.argv[1] + '/left_axis_csv/'
if os.path.isdir(folder_path):
    shutil.rmtree(folder_path)
os.makedirs(folder_path)

SaveData(folder_path + 'left_axis.csv', proxy=plotOverLine1, WriteAllTimeSteps=1)

# set active source
SetActiveSource(slice1)

# set active source
SetActiveSource(plotOverLine1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [1.9995239973068237, -7.970577794628326, 0.5]
renderView1.CameraFocalPoint = [1.9995239973068237, 0.0, 0.5]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 2.062937333721059

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).