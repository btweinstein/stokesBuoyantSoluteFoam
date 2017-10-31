#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
import sys

# create a new 'OpenFOAMReader'
simulation = OpenFOAMReader(FileName=sys.argv[1])

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# set active source
SetActiveSource(None)

# set active source
SetActiveSource(simulation)

# Properties modified on j_m_colony_sweep_0p10foam
simulation.MeshRegions = ['internalMesh', 'yeast_top', 'yeast_bottom', 'petri_top', 'petri_outer', 'petri_bottom']
simulation.CellArrays = ['U', 'c', 'p', 'p_rgh']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1031, 683]

# show data in view
simulation_display = Show(simulation, renderView1)
# trace defaults for the display properties.
simulation_display.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
simulation_display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

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
Hide(simulation, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# reset view to fit data
renderView1.ResetCamera()

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'U', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')

# get color legend/bar for uLUT in view renderView1
uLUTColorBar = GetScalarBar(uLUT, renderView1)

# change scalar bar placement
uLUTColorBar.Position = [0.3308535402521824, 0.7002928257686677]
uLUTColorBar.ScalarBarLength = 0.33000000000000007

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [1.9995241463184357, -7.681563722463692, 0.5000000186264515]
renderView1.CameraFocalPoint = [1.9995241463184357, 0.0, 0.5000000186264515]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 2.9108284352605613

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).