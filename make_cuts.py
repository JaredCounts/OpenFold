from notcher import *
from layout import *
from slicer import *
from flexurizer import *
from test_slices import *
from vector import *
from output_svg import *
import sys

def make_cuts(stlFile, svgOutput):
	sliceDensity = 2/20

	stl_scale = 0.5
	notch_width = 3

	print("SLICING")
	slices = slice(stlFile, sliceDensity, stl_scale)

	print("GENERATING NOTCHES")
	(notches, notchLabels) = notch(slices)
	
	print("GENERATING FLEXURES")
	flexures = flexurize(slices)

	print("GENERATING LAYOUT")
	offsets = layout(slices, 5, 600)
	
	print("GENERATING SVG")
	output_svg(svgOutput, slices, notches, notchLabels, notch_width, flexures, offsets)

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