from Slice import *
from vector import *
from intersect import *

# input: list of slices
# output:
# 	a dictionary keyed by slices valued to list of line segments of where flexures should be

def flexurize(slices, material_thickness):
	flexures = {}

	flexureToNotchGap = material_thickness * 2
	flexureToFlexureGap = material_thickness
	flexureWidth = material_thickness
	flexureDensity = 1 / (flexureToFlexureGap + flexureWidth)
	flexureToEdgeGap = 2 * material_thickness
	minEdgeToEdgeDistance = flexureToEdgeGap * 2

	for sliceA in slices:
		flexures[sliceA] = []

		# Determine notch positions along intersect axis
		(notchAxisIndex, notchPositions) = getIntersectionLines(sliceA, slices)
		verticalAxisIndex = 1 - notchAxisIndex
		# notch axis is axis perpendicular to direction notches run

		# get range on notch axis
		sliceMin = min_from_segments(sliceA.segments)
		sliceMax = max_from_segments(sliceA.segments)

		notchAxisMin = sliceMin[notchAxisIndex]
		notchAxisMax = sliceMax[notchAxisIndex]
		notchAxisRange = notchAxisMax - notchAxisMin

		# find flexure positions
		# and generate flexures
		flexureDirection = 'up'
		approximateFlexureCount = int((notchAxisMax - notchAxisMin) * flexureDensity)
		flexureInterval = notchAxisRange / approximateFlexureCount
		for i in range(0, approximateFlexureCount):
			x = notchAxisMin + flexureInterval / 2 + i * flexureInterval
			
			minDistanceToNotch = notchAxisRange
			for notchPosition in notchPositions:
				minDistanceToNotch = min(minDistanceToNotch, abs(notchPosition - x))

			if minDistanceToNotch <= flexureToNotchGap:
				continue


			origin = [0,0]
			origin[notchAxisIndex] = x
			origin[verticalAxisIndex] = -99999
			direction =  [0,0]
			direction[verticalAxisIndex] = 1

			intersections = ray_cast_2D(sliceA.segments, origin, direction)

			if intersections is None:
				continue

			if len(intersections) % 2 != 0:
				continue # edge case

			for j in range(0, len(intersections), 2):
				intersectionA = intersections[j]
				intersectionB = intersections[j+1]

				# see if distance is ok
				difference = diff(intersectionB, intersectionA)
				lengthSq = dot(difference, difference)
				if lengthSq < minEdgeToEdgeDistance * minEdgeToEdgeDistance:
					continue

				bottom = []
				top = []

				assert flexureDirection == 'up' or flexureDirection == 'down'
				if flexureDirection == 'up':
					topGap = [0,0]
					topGap[verticalAxisIndex] = flexureToEdgeGap
					bottom = intersectionA
					top = diff(intersectionB, topGap)
					flexureDirection = 'down'
				else:
					bottomGap = [0,0]
					bottomGap[verticalAxisIndex] = flexureToEdgeGap
					bottom = add(intersectionA, bottomGap)
					top = intersectionB
					flexureDirection = 'up'

				segment = (bottom, top)
				flexures[sliceA].append(segment)

	return flexures



# returns tuple (a,b)
# where a is the axis perpendicular to the slice intersections
# and b is the list of positions along a
def getIntersectionLines(slice, slices):
	sliceAxisIndex = slice.axisIndex()

	# get list of slices perpendicular to this one
	perpendicularSlices = []
	for sliceB in slices:
		if sliceB.axisIndex() != sliceAxisIndex:
			perpendicularSlices.append(sliceB)

	# determine horizontal axis
	verticalAxisIndex = vertical_index(slice, perpendicularSlices[0])
	sliceNotchAxisIndex = 0
	if slice.axisIndex() < verticalAxisIndex:
		sliceNotchAxisIndex = 0
	else:
		sliceNotchAxisIndex = 1

	# get list of positions along horizontalAxisIndex
	intersectAxisPositions = []
	for sliceB in perpendicularSlices:
		intersectAxisPositions.append(sliceB.axis_position)

	return (sliceNotchAxisIndex, intersectAxisPositions)