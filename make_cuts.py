from notcher import *
from layout import *
from slicer import *
from flexurizer import *
from test_slices import *
from vector import *

# https://pypi.python.org/pypi/svgwrite/
import svgwrite

def make_cuts(stlFile, svgOutput):
	sliceDensity = 2/10
	print("SLICING")
	slices = slice(stlFile, sliceDensity)

	print("GENERATING NOTCHES")
	notches = notch(slices)
	# flexures = flexurize(slices)

	# for currentSlice in slices:
	 	# slice_notches = notches[currentSlice]
	 	# slice_flexures = flexures[slice]
	 	# currentSlice.segments.extend(slice_notches)
	 	# slice.segments.extend(slice_flexures)

	print("GENERATING LAYOUT")
	offsets = layout(slices, 10, 400)
	
	cutScalingFactor = 2

	print("GENERATING SVG")
	svg = svgwrite.Drawing(svgOutput, profile='tiny')
	for currentSlice in slices:
		offset = offsets[currentSlice]

		# add label
		averagePosition = currentSlice.averagePosition()
		textPosition = mult(add(averagePosition, offset), cutScalingFactor)
		svg.add( 
			svg.text(axisIndexToAxisStr(currentSlice.axisIndex()) + '=' + str(currentSlice.axis_position), 
				x=[textPosition[0]], 
				y=[textPosition[1]],
				stroke=svgwrite.rgb(255, 0, 0, '%'),
				fill=svgwrite.rgb(255, 0, 0, '%')))

		# slice segments
		renderSegments(svg, currentSlice.segments, offset, cutScalingFactor)
		# notches
		renderSegments(svg, notches[currentSlice], offset, cutScalingFactor)

	svg.save()

def axisIndexToAxisStr(axisIndex):
	if axisIndex == 0:
		return 'X'
	elif axisIndex == 1:
		return 'Y'
	elif axisIndex == 2:
		return 'Z'
	else:
		print('invalid axis index', axisIndex)
		assert False

def renderSegments(svg, segments, offset, scale):
	for segment in segments:
			svg.add(svg.line(	mult(add(segment[0], offset), scale), 
								mult(add(segment[1], offset), scale), 
								stroke=svgwrite.rgb(0, 0, 0, '%'), 
								stroke_width=2))

make_cuts('stl-files/cube.stl', 'svg-files/cube.svg')
# make_cuts('stl-files/sphere.stl', 'svg-files/sphere.svg')
# make_cuts('stl-files/pug.stl', 'svg-files/pug.svg')
# make_cuts('stl-files/heart.stl', 'svg-files/heart.svg')