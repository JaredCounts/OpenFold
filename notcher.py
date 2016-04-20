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

			# vertical axis is the axis that the slices are not perpendicular to
			verticalAxis = cross(sliceA.axis, sliceB.axis)
			# determine which vector component is the vertical axis (0 for x, 1 for y, 2 for z)
			verticalIndex = 0
			if verticalAxis[0] != 0:
				verticalIndex = 0
			elif verticalAxis[1] != 0:
				verticalIndex = 1
			else:
				verticalIndex = 2

			sliceAIndex = sliceA.axisIndex()
			sliceBIndex = sliceB.axisIndex()

			# determine intersection point on slice A
			sliceANotchAxisIndex = 0
			if sliceBIndex < verticalIndex:
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
			sliceAIntersections = ray_cast_2D(sliceA.segments, sliceANotchBottomRayOrigin, sliceANotchBottomRayDirection)

			sliceBNotchAxisIndex = 0
			if sliceAIndex < verticalIndex:
				sliceBNotchAxisIndex = 0
			else:
				sliceBNotchAxisIndex = 1
			sliceBVerticalAxisIndex = 1 - sliceBNotchAxisIndex

			sliceBNotchBottomRayOrigin = [0,0]
			sliceBNotchBottomRayOrigin[sliceBNotchAxisIndex] = sliceA.axis_position
			sliceBNotchBottomRayOrigin[sliceBVerticalAxisIndex] = -99999 # really big number
			sliceBNotchBottomRayDirection = [0,0]
			sliceBNotchBottomRayDirection[sliceBVerticalAxisIndex] = 1

			sliceBIntersections = ray_cast_2D(sliceB.segments, sliceBNotchBottomRayOrigin, sliceBNotchBottomRayDirection)

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

# simple test
# slices = test_box()
# print(notch(slices)[slices[0]])
