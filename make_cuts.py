from notcher import *
from layout import *
from slicer import *
from flexurizer import *
from test_slices import *
from util import *

# https://pypi.python.org/pypi/svgwrite/
import svgwrite

def make_cuts(stlFile, svgOutput):
	sliceDensity = 2/10
	slices = slice(stlFile, sliceDensity)

	notches = notch(slices)
	# # flexures = flexurize(slices)

	for currentSlice in slices:
	 	slice_notches = notches[currentSlice]
	# 	#slice_flexures = flexures[slice]
	 	currentSlice.segments.extend(slice_notches)
	# 	#slice.segments.extend(slice_flexures)

	segments = layout(slices, 10, 400)
	
	cutScalingFactor = 2

	svg = svgwrite.Drawing(svgOutput, profile='tiny')
	for segment in segments:
		svg.add(svg.line(
						mult(segment[0], cutScalingFactor), 
						mult(segment[1], cutScalingFactor), 
						stroke=svgwrite.rgb(0, 0, 0, '%'), 
						stroke_width=2))
	svg.save()

make_cuts('pug.stl', 'test.svg')