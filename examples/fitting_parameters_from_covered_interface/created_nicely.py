# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.2.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/bryan/git/stokesBuoyantSoluteFoam/examples/fitting_parameters_from_covered_interface')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
O_1 = geompy.MakeVertex(0, 0, 0)
OX_1 = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY_1 = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ_1 = geompy.MakeVectorDXDYDZ(0, 0, 1)
geomObj_1 = geompy.MakeFaceHW(1, 6.11, 3)
geompy.TranslateDXDYDZ(geomObj_1, 3.055, 0, 0.5)
geomObj_2 = geompy.MakeVertex(0, 0, 1)
geomObj_3 = geompy.MakeVertex(0.451, 0, 1)
geomObj_4 = geompy.MakeVertex(0.451, 0, 0)
geomObj_5 = geompy.MakeLineTwoPnt(O_1, geomObj_4)
geomObj_6 = geompy.MakeLineTwoPnt(geomObj_2, geomObj_3)
domain_partitioned = geompy.MakePartition([geomObj_1, geomObj_5, geomObj_6], [], [], [], geompy.ShapeType["FACE"], 0, [], 0)
[axis,yeast_bottom,yeast_top,petri_bottom,petri_top,petri_outer] = geompy.ExtractShapes(domain_partitioned, geompy.ShapeType["EDGE"], True)
[geomObj_7] = geompy.SubShapes(domain_partitioned, [6])
main_face = geompy.CreateGroup(domain_partitioned, geompy.ShapeType["FACE"])
geompy.UnionIDs(main_face, [1])
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( O_1, 'O' )
geompy.addToStudy( OX_1, 'OX' )
geompy.addToStudy( OY_1, 'OY' )
geompy.addToStudy( OZ_1, 'OZ' )
geompy.addToStudy( domain_partitioned, 'domain_partitioned' )
geompy.addToStudyInFather( domain_partitioned, axis, 'axis' )
geompy.addToStudyInFather( domain_partitioned, yeast_bottom, 'yeast_bottom' )
geompy.addToStudyInFather( domain_partitioned, yeast_top, 'yeast_top' )
geompy.addToStudyInFather( domain_partitioned, petri_bottom, 'petri_bottom' )
geompy.addToStudyInFather( domain_partitioned, petri_top, 'petri_top' )
geompy.addToStudyInFather( domain_partitioned, petri_outer, 'petri_outer' )
geompy.addToStudyInFather( domain_partitioned, main_face, 'main_face' )

###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
domain_partitioned_mesh = smesh.Mesh(domain_partitioned)
left_sym = domain_partitioned_mesh.GroupOnGeom(main_face,'main_face',SMESH.FACE)
Quadrangle_2D_1 = domain_partitioned_mesh.Quadrangle(algo=smeshBuilder.QUADRANGLE)
Regular_1D_2 = domain_partitioned_mesh.Segment(geom=axis)
Arithmetic1D_0_01804 = Regular_1D_2.Arithmetic1D(0.01804,0.01,[ 6 ])
Arithmetic1D_0_01804.SetObjectEntry( "domain_partitioned" )
Projection_1D_3 = domain_partitioned_mesh.Projection1D(geom=petri_outer)
ProjectionSource1D_0 = Projection_1D_3.SourceEdge(axis,None,None,None)
Regular_1D_2_1 = domain_partitioned_mesh.Segment(geom=yeast_top)
LocalLength_0_01804 = Regular_1D_2_1.LocalLength(0.01804,None,1e-07)
Projection_1D_3_1 = domain_partitioned_mesh.Projection1D(geom=yeast_bottom)
ProjectionSource1D_0_1 = Projection_1D_3_1.SourceEdge(yeast_top,None,None,None)
Regular_1D_2_2 = domain_partitioned_mesh.Segment(geom=petri_top)
Arithmetic1D_0_01804_1 = Regular_1D_2_2.Arithmetic1D(0.01804,0.01,[])
Arithmetic1D_0_01804_1.SetObjectEntry( "domain_partitioned" )
Projection_1D_3_2 = domain_partitioned_mesh.Projection1D(geom=petri_bottom)
ProjectionSource1D_0_2 = Projection_1D_3_2.SourceEdge(petri_top,None,None,None)
status = domain_partitioned_mesh.RemoveHypothesis(Projection_1D_3,petri_bottom)
status = domain_partitioned_mesh.RemoveHypothesis(ProjectionSource1D_0_2,petri_bottom)
status = domain_partitioned_mesh.RemoveHypothesis(Regular_1D_2,petri_top)
status = domain_partitioned_mesh.RemoveHypothesis(Arithmetic1D_0_01804_1,petri_top)
status = domain_partitioned_mesh.RemoveHypothesis(Projection_1D_3,yeast_bottom)
status = domain_partitioned_mesh.RemoveHypothesis(ProjectionSource1D_0_1,yeast_bottom)
status = domain_partitioned_mesh.RemoveHypothesis(Regular_1D_2,yeast_top)
status = domain_partitioned_mesh.RemoveHypothesis(LocalLength_0_01804,yeast_top)
status = domain_partitioned_mesh.RemoveHypothesis(Projection_1D_3,petri_outer)
status = domain_partitioned_mesh.RemoveHypothesis(ProjectionSource1D_0,petri_outer)
status = domain_partitioned_mesh.RemoveHypothesis(Regular_1D_2,axis)
status = domain_partitioned_mesh.RemoveHypothesis(Arithmetic1D_0_01804,axis)
#domain_partitioned_mesh.GetMesh().RemoveSubMesh( smeshObj_1 ) ### smeshObj_1 has not been yet created
#domain_partitioned_mesh.GetMesh().RemoveSubMesh( smeshObj_2 ) ### smeshObj_2 has not been yet created
#domain_partitioned_mesh.GetMesh().RemoveSubMesh( smeshObj_3 ) ### smeshObj_3 has not been yet created
#domain_partitioned_mesh.GetMesh().RemoveSubMesh( smeshObj_4 ) ### smeshObj_4 has not been yet created
#domain_partitioned_mesh.GetMesh().RemoveSubMesh( smeshObj_5 ) ### smeshObj_5 has not been yet created
#domain_partitioned_mesh.GetMesh().RemoveSubMesh( smeshObj_6 ) ### smeshObj_6 has not been yet created
Regular_1D_2_3 = domain_partitioned_mesh.Segment()
base_mesh_spacing = Regular_1D_2_3.LocalLength(0.01,None,1e-15)
isDone = domain_partitioned_mesh.Compute()
[ smeshObj_7, smeshObj_8, smeshObj_9, smeshObj_10, smeshObj_11, smeshObj_12, left_sym ] = domain_partitioned_mesh.GetGroups()
theNbElems = domain_partitioned_mesh.Evaluate(domain_partitioned)
domain_partitioned_mesh.RotateObject( domain_partitioned_mesh, SMESH.AxisStruct( 0, 0, 0, 0, 0, 1 ), 0.0218166, 0 )
[ yeast_bottom_1, yeast_top_1, petri_bottom_1, petri_top_1, petri_outer_1, smeshObj_13, smeshObj_14, smeshObj_15, smeshObj_16, smeshObj_17, smeshObj_18, right_sym ] = domain_partitioned_mesh.RotationSweepObjects( [ domain_partitioned_mesh ], [ domain_partitioned_mesh ], [ domain_partitioned_mesh ], SMESH.AxisStruct( 0, 0, 0, 0, 0, 1 ), -0.0436332, 1, 1e-15, 1 )
right_sym.SetName( 'right_sym' )
petri_outer_1.SetName( 'petri_outer' )
petri_top_1.SetName( 'petri_top' )
petri_bottom_1.SetName( 'petri_bottom' )
yeast_top_1.SetName( 'yeast_top' )
yeast_bottom_1.SetName( 'yeast_bottom' )
left_sym.SetName( 'left_sym' )
domain_partitioned_mesh.RemoveGroup( smeshObj_13 )
domain_partitioned_mesh.RemoveGroup( smeshObj_18 )
domain_partitioned_mesh.RemoveGroup( smeshObj_17 )
domain_partitioned_mesh.RemoveGroup( smeshObj_16 )
domain_partitioned_mesh.RemoveGroup( smeshObj_15 )
domain_partitioned_mesh.RemoveGroup( smeshObj_14 )

## some objects were removed
aStudyBuilder = theStudy.NewBuilder()
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_17))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_18))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_13))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_16))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_15))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_7))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_9))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_8))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_11))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_10))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_14))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)
SO = theStudy.FindObjectIOR(theStudy.ConvertObjectToIOR(smeshObj_12))
if SO: aStudyBuilder.RemoveObjectWithChildren(SO)

## Set names of Mesh objects
smesh.SetName(Quadrangle_2D_1.GetAlgorithm(), 'Quadrangle_2D_1')
smesh.SetName(Projection_1D_3.GetAlgorithm(), 'Projection_1D_3')
smesh.SetName(Regular_1D_2.GetAlgorithm(), 'Regular_1D_2')
smesh.SetName(ProjectionSource1D_0, 'ProjectionSource1D=0:1:1:9:1,None,None,None')
smesh.SetName(LocalLength_0_01804, 'LocalLength=0.01804,1e-07')
smesh.SetName(Arithmetic1D_0_01804, 'Arithmetic1D=0.01804,0.01,[6],0:1:1:9')
smesh.SetName(ProjectionSource1D_0_2, 'ProjectionSource1D=0:1:1:9:5,None,None,None')
smesh.SetName(base_mesh_spacing, 'base_mesh_spacing')
smesh.SetName(ProjectionSource1D_0_1, 'ProjectionSource1D=0:1:1:9:3,None,None,None')
smesh.SetName(left_sym, 'left_sym')
smesh.SetName(yeast_bottom_1, 'yeast_bottom')
smesh.SetName(Arithmetic1D_0_01804_1, 'Arithmetic1D=0.01804,0.01,[],0:1:1:9')
smesh.SetName(yeast_top_1, 'yeast_top')
smesh.SetName(petri_bottom_1, 'petri_bottom')
smesh.SetName(petri_top_1, 'petri_top')
smesh.SetName(petri_outer_1, 'petri_outer')
smesh.SetName(right_sym, 'right_sym')
smesh.SetName(domain_partitioned_mesh.GetMesh(), 'domain_partitioned_mesh')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
