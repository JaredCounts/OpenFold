from test_slices import *
from util import *

# input: list of slices
# output: a dictionary of slices to line segments of where notches should be
def notch(slices):
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

			



	# for each slice on x axis
		# for each slice on other axis
			# get intersection line
			# determine where along each slice to add segments
	pass

slices = test_box()
print(notch(slices))
