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
		
		for sliceB in slices:

			if sliceB.axis == sliceA.axis:
				continue

			# vertical axis is the axis that the slices are not perpendicular to
			verticalAxis = cross(sliceA.axis, sliceB.axis)
			verticalIndex = 0
			if verticalAxis[0] != 0:
				verticalIndex = 0
			elif verticalAxis[1] != 0:
				verticalIndex = 1
			else:
				verticalIndex = 2

			sliceAIndex = sliceA.axisIndex()
			sliceBIndex = sliceB.axisIndex()

			# sliceA frame of refence
			# where (a,b) is (x,y,z) minus sliceA.axis digit
			# so if sliceA.axis == (0,0,1), then (x,y,z) becomes (x,y)
			
			sliceANotchAxisIndex = 0
			if sliceBIndex < verticalIndex:
				sliceANotchAxisIndex = 0
			else:
				sliceANotchAxisIndex = 1
			sliceAVerticalAxisIndex = 1 - sliceANotchAxisIndex

			print("on slice A, the notch is where the axis", sliceANotchAxisIndex, "is equal to", sliceB.axis_position)

			sliceANotchBottomRayOrigin = [0,0]
			sliceANotchBottomRayOrigin[sliceANotchAxisIndex] = sliceB.axis_position
			sliceANotchBottomRayOrigin[sliceAVerticalAxisIndex] = -99999 # really big number
			sliceANotchBottomRayDirection = [0,0]
			sliceANotchBottomRayDirection[sliceAVerticalAxisIndex] = 1

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

			print(sliceAIntersections)
			print(sliceBIntersections)

slices = test_box()
print(notch(slices))
