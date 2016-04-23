from notcher import *
from layout import *
from slicer import *
from flexurizer import *
from test_slices import *
from vector import *

# https://pypi.python.org/pypi/svgwrite/
import svgwrite

def make_cuts(stlFile, svgOutput):
	sliceDensity = 1/10
	print("SLICING")
	slices = slice(stlFile, sliceDensity)

	print("GENERATING NOTCHES")
	notches = notch(slices)
	# flexures = flexurize(slices)

	print("GENERATING LAYOUT")
	offsets = layout(slices, 10, 400)
	
	cutScalingFactor = 2
	print("GENERATING SVG")
	svg = svgwrite.Drawing(svgOutput, profile='full')

	for currentSlice in slices:
		offset = offsets[currentSlice]

		# add label
		averagePosition = currentSlice.averagePosition()
		textPosition = mult(add(averagePosition, offset), cutScalingFactor)

		svg.add( 
			svg.text(
				axisIndexToAxisStr(currentSlice.axisIndex()) + '=' + str(currentSlice.label), 
				insert=(textPosition[0],textPosition[1]),
				text_anchor='middle',
				font_family="Verdana",
				style="fill: #ff0000; width:1000px; color:red; text-size:15; font-weight:100;"))

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
make_cuts('stl-files/sphere.stl', 'svg-files/sphere.svg')
make_cuts('stl-files/pug.stl', 'svg-files/pug.svg')
# make_cuts('stl-files/heart.stl', 'svg-files/heart.svg')