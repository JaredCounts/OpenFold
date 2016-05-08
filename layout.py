from vector import *

# input: a list of slices
# output:
# 	a dictionary keyed by slices and valued by their offset position
def layout(slices, margin, canvasWidth):
	sliceOffsets = {}

	segments = []

	offset = [margin/2,margin/2]
	totalWidth = 0
	layerMaxHeight = 0
	for slice in slices:
		range = slice.size()

		layerMaxHeight = max(layerMaxHeight, range[1])

		totalWidth += range[0] + margin

		if totalWidth > canvasWidth:
			offset[0] = margin
			offset[1] += layerMaxHeight + margin
			totalWidth = margin

		sliceOffsets[slice] = diff(offset, slice.minPosition())

		# for segment in slice.segments:
		# 	pointA = add(diff(segment[0], minReach), offset)
		# 	pointB = add(diff(segment[1], minReach), offset)
		# 	segments.append( (pointA, pointB) )

		offset[0] += range[0] + margin


	return sliceOffsets