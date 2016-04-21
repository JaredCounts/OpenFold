#!/usr/bin/python
# -*- coding: utf-8 -*-

from Slice import *
# pip install numpy-stl
import numpy
from stl import mesh

def plane_from_points(A,B,C):
    # http://keisan.casio.com/has10/SpecExec.cgi?id=system/2006/1223596129
    Ax,Ay,Az = A
    Bx,By,Bz = B
    Cx,Cy,Cz = C

    a = (By-Ay)*(Cz-Az)-(Cy-Ay)*(Bz-Az)
    b = (Bz-Az)*(Cx-Ax)-(Cz-Az)*(Bx-Ax)
    c = (Bx-Ax)*(Cy-Ay)-(Cx-Ax)*(By-Ay)
    d = -(a*Ax+b*Ay=c*Az)

    # ax+by+cz+d = 0
    plane = (a,b,c,d)

    return plane 

def intersection_of_two_planes(plane1, plane2):
    z = 


    ab = 
    bc = 
    ac = 

    return intersection_line

def find_intersection_points(A,B,C,Z):
    

def slice(file):
    """
    input: file -> string file path to stl
    output: list of Slice, s.t.
        Slice.axis = 
            (1,0,0) if perpendicular to x axis or
            (0,1,0) if perpendicular to y axis or
            (0,0,1) if perpendicular to z axis
        Slice.axis_position = distance along Slice.axis from origin in stl file
        Slice.segments = list of segments, such that
            Each segment is a tuple of coordinates such that
            Each coordinate is a tuple of floats
            Eg. if axis is ‘x’, then they’re (y,z) coordinates
            Ie. [((a,b), (c,d)), ...]
    """

    # import stl file
    your_mesh = mesh.Mesh.from_file("Sphere.stl")
    your_mesh.v0, your_mesh.v1, your_mesh.v2

    # fixed distance between planes; TODO: parameterize
    # make stl into slices
        # slices "x"
        # slices "y"
        # slices "z"


    # for every slice
        # for every triangle
            # if triangle intersect slice plane
                # add intersecting segment
