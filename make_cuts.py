from notcher import *
from layout import *
from slicer import *
from flexurizer import *
from test_slices import *
from vector import *

# https://pypi.python.org/pypi/svgwrite/
import svgwrite
import sys

def make_cuts(stlFile, svgOutput):
	sliceDensity = 2/20

	stl_scale = 0.5

	print("SLICING")
	slices = slice(stlFile, sliceDensity, stl_scale)

	print("GENERATING NOTCHES")
	(notches, notchLabels) = notch(slices)
	
	print("GENERATING FLEXURES")
	flexures = flexurize(slices)

	print("GENERATING LAYOUT")
	offsets = layout(slices, 20, 800)
	
	print("GENERATING SVG")
	svg = svgwrite.Drawing(svgOutput, profile='full')

	for currentSlice in slices:
		offset = offsets[currentSlice]

		# add label
		averagePosition = currentSlice.averagePosition()
		textPosition = add(averagePosition, offset)

		svg.add( 
			svg.text(
				axisIndexToAxisStr(currentSlice.axisIndex()) + str(currentSlice.label), 
				insert=(textPosition[0],textPosition[1]),
				text_anchor='middle',
				font_family="Verdana",
				font_size=12,
				style="fill: #ff0000; width:1000px; color:red; font-weight:100;"))


		# notch labels
		for i in range(0,len(notches[currentSlice])):
			currentNotch = notches[currentSlice][i]
			label = notchLabels[currentSlice][i]
			position = add(mult(add(currentNotch[0], currentNotch[1]), 0.5), offset)
			svg.add( 
				svg.text(
					label, 
					insert=(position[0],position[1]),
					text_anchor='middle',
					font_family="Verdana",
					font_size=10,
					style="fill: #ff0000; width:1000px; color:red; font-weight:50;"))
		# notches
		renderRects(svg, notches[currentSlice], offset)
		
		# flexures
		renderSegments(svg, flexures[currentSlice], offset)
		
		# slice segments
		renderSegments(svg, currentSlice.segments, offset)
		

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

def renderRects(svg, segments, offset):
	width = 3
	for segment in segments:
		size = diff(segment[1], segment[0])
		centering = [0,0]
		if size[0] == 0:
			size[0] = width
			centering[0] = -width/2
		if size[1] == 0:
			size[1] = width
			centering[1] = -width/2
		svg.add(svg.rect(insert=(add(add(segment[0], centering), offset)), 
						 size=size))

def renderSegments(svg, segments, offset):
	for segment in segments:
			svg.add(svg.line(add(segment[0], offset), 
							 add(segment[1], offset), 
							 stroke=svgwrite.rgb(0, 0, 0, '%'), 
							 stroke_width=1,
							 stroke_linecap="square"))

if len(sys.argv) != 3:
	print("Usage: python make_cuts.py stl_file_path svg_output_file_path")
else:
	stlFile = sys.argv[1]
	svgOutput = sys.argv[2]
	make_cuts(stlFile, svgOutput)

# make_cuts('stl-files/cube.stl', 'svg-files/cube.svg')
# make_cuts('stl-files/chair.stl', 'svg-files/chair.svg') # http://www.thingiverse.com/thing:141703
# make_cuts('stl-files/rhino.stl', 'svg-files/rhino.svg')
# make_cuts('stl-files/bunny.stl', 'svg-files/bunny.svg')
# make_cuts('stl-files/sphere.stl', 'svg-files/sphere.svg')
# make_cuts('stl-files/pug.stl', 'svg-files/pug.svg')
# make_cuts('stl-files/heart.stl', 'svg-files/heart.svg')