from vector import *
from intersect import *

class Slice(object):
	def __init__(self):
		self.axis = (1,0,0)
		self.axis_position = 0
		self.segments = []
		self.label = 0

	def minPosition(self):
		return min_from_segments(self.segments)

	def maxPosition(self):
		return max_from_segments(self.segments)

	def size(self):
		return diff(self.maxPosition(), self.minPosition())

	def averagePosition(self):
		positionSum = (0,0)
		for segment in self.segments:
			positionSum = add(positionSum, segment[0])
			positionSum = add(positionSum, segment[1])
		return mult(positionSum, 1.0/(len(self.segments)*2))

	# get index of axis this slice is perpendicular to
	# eg, if it is perpendicular to (0,1,0), 
	# 	then 1 is returned since the y axis is at index 1
	def axisIndex(self):
		index = 0
		if self.axis[0] != 0:
			index = 0
		elif self.axis[1] != 0:
			index = 1
		else:
			assert self.axis[2] != 0
			index = 2
		return index

	# returns all the edge and vertex points on self that intersect with sliceB
	# 	in self's frame of reference (ie. (x,y) corresponds to the (x,y) axes in self)
	def intersect(self, sliceB):
		verticalIndex = vertical_index(self, sliceB)
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
		return ray_cast_2D(self.segments, sliceANotchBottomRayOrigin, sliceANotchBottomRayDirection)

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

def min_from_segments(segments):
	minX = float("inf")
	minY = float("inf")
	for segment in segments:
		pointA = segment[0]
		pointB = segment[1]
		minX = min(minX, pointA[0])
		minX = min(minX, pointB[0])
		minY = min(minY, pointA[1])
		minY = min(minY, pointB[1])

	return (minX, minY)

def max_from_segments(segments):
	maxX = -float("inf")
	maxY = -float("inf")

	for segment in segments:
		pointA = segment[0]
		pointB = segment[1]
		maxX = max(maxX, pointA[0])
		maxX = max(maxX, pointB[0])
		maxY = max(maxY, pointA[1])
		maxY = max(maxY, pointB[1])

	return (maxX, maxY)