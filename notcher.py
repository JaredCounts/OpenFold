from test_slices import *
from vector import *
from intersect import *

# input: list of slices
# output: 
#  a tuple such that
#  	the first element is a dictionary keyed by slices valued to list of line segments of where notches should be
#   the second is a dictionary keyed by slices valued 
# 		to a list with labels (whose indices match notch indices for that slice)
def notch(slices):
	if len(slices) == 0:
		return {}

	# used to determine which notches will be from top and which will be from bottom
	referenceAxis = slices[0].axis

	notches = {}
	labels = {}
	for sliceA in slices:
		# we do every slice pair such that sliceA is on the referenceAxis and sliceB is on the other axis
		if sliceA.axis != referenceAxis:
			continue

		if sliceA not in notches:
			notches[sliceA] = []
			labels[sliceA] = []

		for sliceB in slices:
			# sliceA won't intersect with sliceB if they're on the same axis
			if sliceA.axis == sliceB.axis:
				continue

			if sliceB not in notches:
				notches[sliceB] = []
				labels[sliceB] = []

			# sliceA == the slice with the axis matching the reference axis
			# this way we can ensure we always notch from the same side for slices with the same axis

			# determine all the points on sliceA along the intersection line with sliceB
			sliceAIntersections = sliceA.intersect(sliceB)
			sliceBIntersections = sliceB.intersect(sliceA) 

			if sliceAIntersections is None or sliceBIntersections is None:
				continue

			if len(sliceAIntersections) != len(sliceBIntersections):
				continue
			if len(sliceAIntersections) % 2 != 0:
				continue

			# assume that every pair of intersections on each slice corresponds to a "filled" region
			# (TODO this assumption breaks if the intersection is tangent to some part of the slice)
			overreach = 3 # how much to extend past the edge
			for i in range(0, len(sliceAIntersections), 2):
				sliceAIntersectionA = sliceAIntersections[i]
				sliceAIntersectionB = sliceAIntersections[i+1]
				sliceAMidPoint = mult(add(sliceAIntersectionA, sliceAIntersectionB), 0.5)
				
				direction = norm(diff(sliceAIntersectionA,sliceAIntersectionB))
				sliceANotch = (add(sliceAIntersectionA, mult(direction,overreach)), sliceAMidPoint)
				notches[sliceA].append( sliceANotch )
				labels[sliceA].append(sliceB.label)

				sliceBIntersectionA = sliceBIntersections[i]
				sliceBIntersectionB = sliceBIntersections[i+1]
				sliceBMidPoint = mult(add(sliceBIntersectionA, sliceBIntersectionB), 0.5)

				direction = norm(diff(sliceBIntersectionA,sliceBIntersectionB))

				sliceBNotch = (sliceBMidPoint, diff(sliceBIntersectionB, mult(direction, overreach)))
				notches[sliceB].append( sliceBNotch )
				labels[sliceB].append(sliceA.label)

	return (notches, labels)


# simple test
# slices = test_box()
# print(notch(slices)[slices[0]])
