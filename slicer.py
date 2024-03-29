from Slice import *

from vector import *
from intersect import *

import numpy
from stl import mesh

def slice(stlFile, sliceDensity, stl_scale):
	stlMesh = mesh.Mesh.from_file(stlFile)
	stlMesh.data['vectors'] *= stl_scale
	
	meshMin = stlMesh.min_
	meshMax = stlMesh.max_
	
	meshRange = meshMax - meshMin
	
	# do x and y
	sliceXCount = meshRange[0] * sliceDensity
	sliceYCount = meshRange[1] * sliceDensity

	slices = []

	xInterval = meshRange[0] / int(sliceXCount)
	for xPlane in range(0, int(sliceXCount)):
		print('on x: slicing', xPlane+1, 'out of', int(sliceXCount))
		x = meshMin[0] + xInterval/2 + xPlane * xInterval
		thisSlice = slice_on_plane(stlMesh, 0, x)
		if thisSlice is not None:
			thisSlice.label = xPlane + 1
			slices.append(thisSlice)

	yInterval = meshRange[1] / int(sliceYCount)
	for yPlane in range(0, int(sliceYCount)):
		print('on y: slicing', yPlane+1, 'out of', int(sliceYCount))
		y = meshMin[1] + yInterval / 2 + yPlane * yInterval

		thisSlice = slice_on_plane(stlMesh, 1, y)
		if thisSlice is not None:
			thisSlice.label = yPlane + 1
			slices.append(thisSlice)

	return slices


def slice_on_plane(stlMesh, planeIndex, planePosition):
	sliceSegments = []

	for triangle in stlMesh:

		v0 = triangle[0:3]
		v1 = triangle[3:6]
		v2 = triangle[6:9]

		# skip triangles that don't intersect the plane
		if v0[planeIndex] < planePosition and v1[planeIndex] < planePosition and v2[planeIndex] < planePosition:
			continue
		if v0[planeIndex] > planePosition and v1[planeIndex] > planePosition and v2[planeIndex] > planePosition:
			continue
		if v0[planeIndex] == planePosition and v1[planeIndex] == planePosition and v2[planeIndex] == planePosition:
			# TODO - these points are all coplanar with the slice points
			# so which segments do we add, if any?
			continue

		planePoint = [0,0,0]
		planePoint[planeIndex] = planePosition

		planeNormal = [0,0,0]
		planeNormal[planeIndex] = planePosition

		segment1Intersection = intersect_segment_and_plane(v0.tolist(), v1.tolist(), planePoint, planeNormal)
		segment2Intersection = intersect_segment_and_plane(v0.tolist(), v2.tolist(), planePoint, planeNormal)
		segment3Intersection = intersect_segment_and_plane(v1.tolist(), v2.tolist(), planePoint, planeNormal)

		segment = []
		if segment1Intersection != None:
			# we extract the relevant 2D coefficients
			segment.append(segment1Intersection[:planeIndex] + segment1Intersection[planeIndex+1:])
		if segment2Intersection != None:
			segment.append(segment2Intersection[:planeIndex] + segment2Intersection[planeIndex+1:])
		if segment3Intersection != None:
			segment.append(segment3Intersection[:planeIndex] + segment3Intersection[planeIndex+1:])
		
		if len(segment) == 3: # 3 segments intersect?
			segment.pop() 

		if len(segment) != 2:
			# print("segment not 2 points.", len(segment), "points")
			continue # something weird happened
		sliceSegments.append(segment)

	if len(sliceSegments) == 0:
		print("no segments")
		return None

	thisSlice = Slice()
	thisSlice.axis = [0,0,0]
	thisSlice.axis[planeIndex] = 1
	thisSlice.axis_position = planePosition
	thisSlice.segments = sliceSegments

	return thisSlice

