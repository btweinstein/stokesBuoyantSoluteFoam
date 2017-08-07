# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.2.0 with dump python functionality
###

import sys
import salome

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

import SMESH
from salome.smesh import smeshBuilder


class Yeast_Wedge(object):
    def __init__(self):
        self.petri_radius = 6.25
        self.petri_height = 1.0
        self.yeast_radius = 0.3125
        self.base_mesh_spacing = 0.025
        self.wedge_angle = 2.5

        self.yeast_mesh_spacing = self.yeast_radius/100.

        salome.salome_init()
        self.theStudy = salome.myStudy

        self.smesh = None
        self.mesh = None
        self.geompy = None

        self.main_face_gr = None


    def create_base_mesh(self):

        geompy = geomBuilder.New(self.theStudy)
        self.geompy = geompy

        O = geompy.MakeVertex(0, 0, 0)
        OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
        OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
        OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

        domain = geompy.MakeFaceHW(self.petri_height, self.petri_radius, 3)
        geompy.TranslateDXDYDZ(domain, self.petri_radius/2., 0, self.petri_height/2.)

        top_axis = geompy.MakeVertex(0, 0, self.petri_height)
        yeast_top_extent = geompy.MakeVertex(self.yeast_radius, 0, self.petri_height)
        yeast_bottom_extent = geompy.MakeVertex(self.yeast_radius, 0, 0)

        yeast_bottom_line = geompy.MakeLineTwoPnt(O, yeast_bottom_extent)
        yeast_top_line = geompy.MakeLineTwoPnt(top_axis, yeast_top_extent)

        domain_partitioned = geompy.MakePartition([domain, yeast_bottom_line, yeast_top_line],
                                                  [], [], [], geompy.ShapeType["FACE"], 0, [], 0)

        [axis,yeast_bottom,yeast_top,petri_bottom,petri_top,petri_outer] = \
            geompy.ExtractShapes(domain_partitioned, geompy.ShapeType["EDGE"], True)

        main_face = geompy.CreateGroup(domain_partitioned, geompy.ShapeType["FACE"])

        geompy.UnionIDs(main_face, [1])

        # Now add everything to the study

        geompy.addToStudy( O, 'O' )
        geompy.addToStudy( OX, 'OX' )
        geompy.addToStudy( OY, 'OY' )
        geompy.addToStudy( OZ, 'OZ' )

        geompy.addToStudy( domain_partitioned, 'domain_partitioned' )
        geompy.addToStudyInFather( domain_partitioned, axis, 'axis' )
        geompy.addToStudyInFather( domain_partitioned, yeast_bottom, 'yeast_bottom' )
        geompy.addToStudyInFather( domain_partitioned, yeast_top, 'yeast_top' )
        geompy.addToStudyInFather( domain_partitioned, petri_bottom, 'petri_bottom' )
        geompy.addToStudyInFather( domain_partitioned, petri_top, 'petri_top' )
        geompy.addToStudyInFather( domain_partitioned, petri_outer, 'petri_outer' )
        geompy.addToStudyInFather( domain_partitioned, main_face, 'main_face' )

        if salome.sg.hasDesktop():
          salome.sg.updateObjBrowser(True)

        ##
        ### SMESH component
        ###

        smesh = smeshBuilder.New(self.theStudy)
        self.smesh = smesh

        domain_partitioned_mesh = smesh.Mesh(domain_partitioned)
        self.mesh = domain_partitioned_mesh

        axis_gr = domain_partitioned_mesh.GroupOnGeom(axis,'axis',SMESH.EDGE)
        yeast_bottom_gr = domain_partitioned_mesh.GroupOnGeom(yeast_bottom,'yeast_bottom',SMESH.EDGE)
        yeast_top_gr = domain_partitioned_mesh.GroupOnGeom(yeast_top,'yeast_top',SMESH.EDGE)
        petri_bottom_gr = domain_partitioned_mesh.GroupOnGeom(petri_bottom,'petri_bottom',SMESH.EDGE)
        petri_top_gr = domain_partitioned_mesh.GroupOnGeom(petri_top,'petri_top',SMESH.EDGE)
        petri_outer_gr = domain_partitioned_mesh.GroupOnGeom(petri_outer, 'petri_outer',SMESH.EDGE)
        main_face_gr = domain_partitioned_mesh.GroupOnGeom(main_face,'main_face',SMESH.FACE)
        self.main_face_gr = main_face_gr

        ## Set names of Mesh objects
        smesh.SetName(domain_partitioned_mesh.GetMesh(), 'domain_partitioned_mesh')
        smesh.SetName(main_face_gr, 'main_face')
        smesh.SetName(axis_gr, 'axis')
        smesh.SetName(yeast_top_gr, 'yeast_top')
        smesh.SetName(yeast_bottom_gr, 'yeast_bottom')
        smesh.SetName(petri_top_gr, 'petri_top')
        smesh.SetName(petri_bottom_gr, 'petri_bottom')
        smesh.SetName(petri_outer_gr, 'petri_outer')


        # Use quadrangles
        domain_partitioned_mesh.Quadrangle(algo=smeshBuilder.QUADRANGLE)
        print 'Done creating the basal mesh!'

        # Refine close to the yeast...and far away as well.

        ### Vertical refinement ###
        vertical_refiner = domain_partitioned_mesh.Segment(geom=axis)
        vertical_refiner.Arithmetic1D(self.yeast_mesh_spacing, self.base_mesh_spacing, [6]) # Reverse edge #6
        axis_submesh = vertical_refiner.GetSubMesh()
        smesh.SetName(axis_submesh, 'axis_submesh')

        # Project the axis submesh onto the far wall
        outer_projection = domain_partitioned_mesh.Projection1D(geom=petri_outer)
        outer_projection.SourceEdge(axis, None, None, None)
        outer_submesh = outer_projection.GetSubMesh()
        smesh.SetName(outer_submesh, 'outer_submesh')

        ### Horizontal Refinement ###

        # Refine yeast
        yeast_refiner = domain_partitioned_mesh.Segment(geom=yeast_top)
        yeast_refiner.LocalLength(self.yeast_mesh_spacing)
        yeast_top_submesh = yeast_refiner.GetSubMesh()
        smesh.SetName(yeast_top_submesh, 'yeast_top_submesh')

        # Project yeast_top onto yeast_bottom
        yeast_projection = domain_partitioned_mesh.Projection1D(geom=yeast_bottom)
        yeast_projection.SourceEdge(yeast_top, None, None, None)
        yeast_bottom_submesh = yeast_projection.GetSubMesh()
        smesh.SetName(yeast_bottom_submesh, 'yeast_bottom_submesh')

        # Refine rest of the top & bottom
        petri_refiner = domain_partitioned_mesh.Segment(geom=petri_top)
        petri_refiner.Arithmetic1D(self.yeast_mesh_spacing, self.base_mesh_spacing, [])
        petri_top_submesh = petri_refiner.GetSubMesh()
        smesh.SetName(petri_top_submesh, 'petri_top_submesh')

        # Project onto the bottom from the top
        petri_project = domain_partitioned_mesh.Projection1D(geom=petri_bottom)
        petri_project.SourceEdge(petri_top, None, None, None)
        petri_bottom_submesh = petri_project.GetSubMesh()
        smesh.SetName(petri_bottom_submesh, 'petri_bottom_submesh')

        domain_partitioned_mesh.Compute()
        if salome.sg.hasDesktop():
          salome.sg.updateObjBrowser(True)

        print 'Done computing the refined mesh!'

    def extrude_mesh(self):

        domain_partitioned_mesh = self.mesh
        smesh = self.smesh
        main_face_gr = self.main_face_gr

        ### EXTRUDE MESH ###

        z_rotation = SMESH.AxisStruct(0, 0, 0, 0, 0, 1)
        wedge_angle_in_rad = (self.wedge_angle/180.) * math.pi

        # Rotate the mesh half of a wedge angle
        domain_partitioned_mesh.RotateObject(domain_partitioned_mesh, z_rotation, .5*wedge_angle_in_rad, 0)

        # Extrude the mesh to create the wedge
        [yeast_bottom_face, yeast_top_face, petri_bottom_face, petri_top_face, petri_outer_face, whole_volume,
         yeast_bottom_top_EDGE, yeast_top_top_EDGE, petri_bottom_top_EDGE, petri_top_top_EDGE,
         petri_outer_top_EDGE, right_sym_face] = \
            domain_partitioned_mesh.RotationSweepObjects([domain_partitioned_mesh], [domain_partitioned_mesh],
                                                         [domain_partitioned_mesh],
                                                         z_rotation, -wedge_angle_in_rad, 1, 1e-15, 1)

        smesh.SetName(right_sym_face, 'right_sym')
        right_sym_face.SetName('right_sym')

        smesh.SetName(petri_outer_face, 'petri_outer')
        petri_outer_face.SetName('petri_outer')

        smesh.SetName(petri_top_face, 'petri_top')
        petri_top_face.SetName('petri_top')

        smesh.SetName(petri_bottom_face, 'petri_bottom')
        petri_bottom_face.SetName('petri_bottom')

        smesh.SetName(yeast_top_face, 'yeast_top')
        yeast_top_face.SetName('yeast_top')

        smesh.SetName(yeast_bottom_face, 'yeast_bottom')
        yeast_bottom_face.SetName('yeast_bottom')

        smesh.SetName(main_face_gr, 'left_sym')
        main_face_gr.SetName('left_sym')

        print 'Done extruding geometry!'

        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser(True)