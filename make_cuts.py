from notcher import *
from layout import *
from slicer import *
from flexurizer import *
from test_slices import *
from util import *

# https://pypi.python.org/pypi/svgwrite/
import svgwrite

def make_cuts(stlFile, svgOutput):
	# slices = slice(file)
	slices = test_box() # placeholder
	notches = notch(slices)
	# flexures = flexurize(slices)

	for slice in slices:
		slice_notches = notches[slice]
		#slice_flexures = flexures[slice]
		slice.segments.extend(slice_notches)
		#slice.segments.extend(slice_flexures)

	segments = layout(slices, 10)
	
	svg = svgwrite.Drawing(output, profile='tiny')
	for segment in segments:
		svg.add(svg.line(
						segment[0], 
						segment[1], 
						stroke=svgwrite.rgb(0, 0, 0, '%'), 
						stroke_width=4))
	svg.save()

make_cuts('', 'test.svg')