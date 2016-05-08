
# https://pypi.python.org/pypi/svgwrite/
import svgwrite
from vector import *

def output_svg(svgOutput, slices, notches, notchLabels, material_thickness, flexures, offsets):
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
		renderRects(svg, notches[currentSlice], offset, material_thickness)
		
		# flexures
		renderRects(svg, flexures[currentSlice], offset, material_thickness)
		
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

def renderRects(svg, segments, offset, width):
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
