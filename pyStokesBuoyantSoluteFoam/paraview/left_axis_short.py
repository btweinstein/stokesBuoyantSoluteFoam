from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

my_foam = FindSource("case.foam")
SetActiveSource(my_foam)

tsteps = my_foam.TimestepValues
PlotOverLine1 = PlotOverLine( Source="High Resolution Line Source" )
DataRepresentation7 = Show()

PlotOverLine1.Source.Point1 = [-0.052, 0.0, 0.0]
PlotOverLine1.Source.Point2 = [0.0, 0.0, 0.0]

source = PlotOverLine1

for TimeStepNum in range(0,len(tsteps)):
    view = GetActiveView()
    view.ViewTime = tsteps[TimeStepNum]
    Render()
    writer = CreateWriter("file_%d.csv" %(TimeStepNum), source)
    writer.FieldAssociation = "Points"
    writer.UpdatePipeline()
    Render()
    del writer