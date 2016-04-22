from vector import *

# input: a list of slices
# output:
# 	a list of line segments
# 	all in a single frame of reference
def layout(slices, margin, canvasWidth):
	segments = []

	offset = [margin,margin]
	totalWidth = 0
	layerMaxHeight = 0
	for slice in slices:
		minReach = min_from_segments(slice.segments)
		maxReach = max_from_segments(slice.segments)
		range = diff(maxReach, minReach)

		layerMaxHeight = max(layerMaxHeight, range[1])

		totalWidth += range[0] + margin

		if totalWidth > canvasWidth:
			offset[0] = margin
			offset[1] += layerMaxHeight + margin
			totalWidth = margin

		for segment in slice.segments:
			pointA = add(diff(segment[0], minReach), offset)
			pointB = add(diff(segment[1], minReach), offset)
			segments.append( (pointA, pointB) )

		offset[0] += range[0] + margin

	return segments

def min_from_segments(segments):
	minX = float("inf")
	minY = float("inf")
	for segment in segments:
		pointA = segment[0]
		pointB = segment[1]
		minX = min(minX, pointA[0])
		minX = min(minX, pointB[0])
		minY = min(minY, pointA[0])
		minY = min(minY, pointB[0])

	return (minX, minY)

def max_from_segments(segments):
	maxX = -float("inf")
	maxY = -float("inf")

	for segment in segments:
		pointA = segment[0]
		pointB = segment[1]
		maxX = max(maxX, pointA[0])
		maxX = max(maxX, pointB[0])
		maxY = max(maxY, pointA[0])
		maxY = max(maxY, pointB[0])

	return (maxX, maxY)