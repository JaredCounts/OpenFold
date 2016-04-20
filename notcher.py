from test_slices import *
from util import *

# input: list of slices
# output: a dictionary of slices to line segments of where notches should be
def notch(slices):
	if len(slices) == 0:
		return {}

	# used to determine which notches will be from top and which will be from bottom
	referenceAxis = slices[0].axis

	notches = {}
	for sliceA in slices:
		# we do every slice pair such that sliceA is on the referenceAxis and sliceB is on the other axis
		if sliceA.axis != referenceAxis:
			continue

		if sliceA not in notches:
			notches[sliceA] = []

		for sliceB in slices:
			# sliceA won't intersect with sliceB if they're on the same axis
			if sliceA.axis == sliceB.axis:
				continue

			if sliceB not in notches:
				notches[sliceB] = []

			# sliceA == the slice with the axis matching the reference axis
			# this way we can ensure we always notch from the same side for slices with the same axis

			# determine all the points on sliceA along the intersection line with sliceB
			sliceAIntersections = slice_intersections_on_first(sliceA, sliceB)
			sliceBIntersections = slice_intersections_on_first(sliceB, sliceA) 

			for i in range(0, len(sliceAIntersections), 2):
				sliceAIntersectionA = sliceAIntersections[i]
				sliceAIntersectionB = sliceAIntersections[i+1]
				sliceAMidPoint = mult(add(sliceAIntersectionA, sliceAIntersectionB), 0.5)
				notches[sliceA].append( (sliceAIntersectionA, sliceAMidPoint) )

				sliceBIntersectionA = sliceBIntersections[i]
				sliceBIntersectionB = sliceBIntersections[i+1]
				sliceBMidPoint = mult(add(sliceBIntersectionA, sliceBIntersectionB), 0.5)
				notches[sliceB].append( (sliceBMidPoint, sliceBIntersectionB) )

	return notches

# returns the vector component index of the vertical direction for two intersecting slices
# eg, if sliceA lies along the X plane, sliceB lies along the Y plane, then this will return 2 for Z
def vertical_index(sliceA, sliceB):
	verticalAxis = cross(sliceA.axis, sliceB.axis)
	# determine which vector component is the vertical axis (0 for x, 1 for y, 2 for z)
	verticalIndex = 0
	if verticalAxis[0] != 0:
		verticalIndex = 0
	elif verticalAxis[1] != 0:
		verticalIndex = 1
	else:
		verticalIndex = 2
	return verticalIndex

# given sliceA and sliceB slices
# returns all the edge and vertex points on sliceA that intersect with sliceB
# 	in sliceA's frame of reference (ie. (x,y) corresponds to the (x,y) axes in sliceA)
def slice_intersections_on_first(sliceA, sliceB):
	verticalIndex = vertical_index(sliceA, sliceB)
	# determine intersection point on slice A
	sliceANotchAxisIndex = 0
	if sliceB.axisIndex() < verticalIndex:
		sliceANotchAxisIndex = 0
	else:
		sliceANotchAxisIndex = 1
	sliceAVerticalAxisIndex = 1 - sliceANotchAxisIndex

	# sliceB intersects sliceA where sliceANotchAxisIndex vector component equals sliceB.axis_position (in sliceA's frame of reference)

	sliceANotchBottomRayOrigin = [0,0]
	sliceANotchBottomRayOrigin[sliceANotchAxisIndex] = sliceB.axis_position
	sliceANotchBottomRayOrigin[sliceAVerticalAxisIndex] = -99999 # really big number
	sliceANotchBottomRayDirection = [0,0]
	sliceANotchBottomRayDirection[sliceAVerticalAxisIndex] = 1

	# determine all the points on sliceA along the intersection line with sliceB
	return ray_cast_2D(sliceA.segments, sliceANotchBottomRayOrigin, sliceANotchBottomRayDirection)

# simple test
# slices = test_box()
# print(notch(slices)[slices[0]])
