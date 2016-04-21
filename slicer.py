from Slice import *

import numpy
from stl import mesh

def slice(stlFile, sliceDensity):
	stlMesh = mesh.Mesh.from_file(stlFile)
	
	meshMin = stlMesh.min_
	meshMax = stlMesh.max_
	
	meshRange = meshMax - meshMin
	
	# do x and y
	sliceXCount = meshRange[0] * sliceDensity
	sliceYCount = meshRange[1] * sliceDensity

	slices = []

	for xPlane in range(0, int(sliceXCount)):
		print('on x: slicing', xPlane, 'out of', int(sliceXCount))
		x = xPlane * meshRange[0] / int(sliceXCount)
		thisSlice = slice_on_plane(stlMesh, 0, x)
		if thisSlice is not None:
			slices.append(thisSlice)

	for yPlane in range(0, int(sliceYCount)):
		print('on y: slicing', yPlane, 'out of', int(sliceYCount))
		y = yPlane * meshRange[1] / int(sliceYCount)

		thisSlice = slice_on_plane(stlMesh, 1, y)
		if thisSlice is not None:
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

		if len(segment) != 2:
			# print("segment not 2 points.", len(segment), "points")
			continue # something weird happened
		sliceSegments.append(segment)

	if len(sliceSegments) == 0:
		return None

	thisSlice = Slice()
	thisSlice.axis = [0,0,0]
	thisSlice.axis[planeIndex] = 1
	thisSlice.axis_position = planePosition
	thisSlice.segments = sliceSegments

	return thisSlice

# see if point is between the segment points
def colinear_point_on_segment(point, segmentPointA, segmentPointB):
	pointToSegA = diff(point, segmentPointA)
	pointToSegB = diff(point, segmentPointB)
	segAToSegB = diff(segmentPointA, segmentPointB)

	return dot(pointToSegA, pointToSegA) + dot(pointToSegB, pointToSegB) - dot(segAToSegB, segAToSegB) < 0.001

def intersect_segment_and_plane(segmentPointA, segmentPointB, planePoint, planeNormal):
	segmentDirection = diff(segmentPointB, segmentPointA)


	intersection = intersect_line_and_plane(segmentPointA, segmentDirection, planePoint, planeNormal)
	
	if intersection is None:
		return None

	if not colinear_point_on_segment(intersection, segmentPointA, segmentPointB):
		return None

	return intersection

# assuming plane is axis-aligned and lies on planeIndex axis
def intersect_line_and_plane(linePoint, lineDirection, planePoint, planeNormal):
	lineToPlaneCosine = numpy.dot(lineDirection, planeNormal)

	if lineToPlaneCosine == 0:
		return None # coplanar

	lineToPlane = diff(planePoint, linePoint)
	
	factorAlongLine = dot(lineToPlane, planeNormal) / lineToPlaneCosine

	return add(linePoint, mult(lineDirection, factorAlongLine))


# slices = slice('pug.stl', 1/10)
# print(len(slices))
# print(slices[0])