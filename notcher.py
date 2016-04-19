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
			print(verticalAxis)



	# for each slice on x axis
		# for each slice on other axis
			# get intersection line
			# determine where along each slice to add segments
	pass

slices = test_box()
print(notch(slices))
