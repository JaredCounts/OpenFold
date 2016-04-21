from notcher import *
from layout import *
from slicer import *
from flexurizer import *
from test_slices import *
from util import *

# https://pypi.python.org/pypi/svgwrite/
import svgwrite

def make_cuts(stlFile, svgOutput):
	sliceDensity = 5/10
	print("SLICING")
	slices = slice(stlFile, sliceDensity)

	print("GENERATING NOTCHES")
	notches = notch(slices)
	# flexures = flexurize(slices)

	for currentSlice in slices:
	 	slice_notches = notches[currentSlice]
	 	# slice_flexures = flexures[slice]
	 	currentSlice.segments.extend(slice_notches)
	 	# slice.segments.extend(slice_flexures)

	print("GENERATING LAYOUT")
	segments = layout(slices, 10, 400)
	
	cutScalingFactor = 2

	print("GENERATING SVG")
	svg = svgwrite.Drawing(svgOutput, profile='tiny')
	for segment in segments:
		svg.add(svg.line(	mult(segment[0], cutScalingFactor), 
							mult(segment[1], cutScalingFactor), 
							stroke=svgwrite.rgb(0, 0, 0, '%'), 
							stroke_width=2))
	svg.save()

make_cuts('stl-files/cube.stl', 'svg-files/cube.svg')
make_cuts('stl-files/sphere.stl', 'svg-files/sphere.svg')
make_cuts('stl-files/pug.stl', 'svg-files/pug.svg')
make_cuts('stl-files/heart.stl', 'svg-files/heart.svg')