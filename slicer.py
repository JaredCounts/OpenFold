from Slice import *

import numpy
from stl import mesh

def slice(stlFile, sliceDensity):
	stlMesh = mesh.Mesh.from_file(stlFile)
	
	meshMin = stlMesh.min_
	meshMax = stlMesh.max_
	
	meshRange = meshMax - meshMin
	
	# do x
	sliceXCount = meshRange[0] * sliceDensity

	slices = []

	# we choose two directions to slice from
	sliceDirection = (1,0,0)
	sliceIndex = 0

	for xPlane in range(0, int(sliceXCount)):
		print('slicing', xPlane, 'out of', int(sliceXCount))
		x = xPlane * meshRange[0] / int(sliceXCount)
		
		sliceSegments = []

		for triangle in stlMesh:

			v0 = triangle[0:3]
			v1 = triangle[3:6]
			v2 = triangle[6:9]

			# skip triangles that don't intersect the plane
			if v0[0] < x and v1[0] < x and v2[0] < x:
				continue
			if v0[0] > x and v1[0] > x and v2[0] > x:
				continue
			if v0[0] == x and v1[0] == x and v2[0] == x:
				continue

			planePoint = [x,0,0]
			planeNormal = [1,0,0]

			segment1Intersection = intersect_segment_and_plane(v0.tolist(), v1.tolist(), planePoint, planeNormal)
			segment2Intersection = intersect_segment_and_plane(v0.tolist(), v2.tolist(), planePoint, planeNormal)
			segment3Intersection = intersect_segment_and_plane(v1.tolist(), v2.tolist(), planePoint, planeNormal)

			segment = []
			if segment1Intersection != None:
				segment.append(segment1Intersection[1:3])
			if segment2Intersection != None:
				segment.append(segment2Intersection[1:3])
			if segment3Intersection != None:
				segment.append(segment3Intersection[1:3])

			if len(segment) != 2:
				# print("segment not 2 points.", len(segment), "points")
				continue # something weird happened

			sliceSegments.append(segment)

		thisSlice = Slice()
		thisSlice.axis = (1,0,0)
		thisSlice.axis_position = x
		thisSlice.segments = sliceSegments
		slices.append(thisSlice)

	return slices

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