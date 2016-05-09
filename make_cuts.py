from notcher import *
from layout import *
from slicer import *
from flexurizer import *
from test_slices import *
from vector import *
from output_svg import *
from read_ini import *
import math
import sys

import pygame
 
def visualizer(slices, notches, flexures):
	average = [0,0,0]
	pointCount = 0
	for slice in slices:
		for segment in slice.segments:
			startPoint = segment[0].copy()
			endPoint = segment[1].copy()
			startPoint.insert(slice.axisIndex(), slice.axis_position)
			endPoint.insert(slice.axisIndex(), slice.axis_position)
			average = add(average, startPoint)
			average = add(average, endPoint)
			pointCount += 2

	average = mult(average, 1.0 / pointCount)

	# initialize game engine
	pygame.init()
	# set screen width/height and caption
	size = [640, 480]
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption('My Game')
	# initialize clock. used later in the loop.
	clock = pygame.time.Clock()

	rotateX = 0

	# Loop until the user clicks close button
	done = False
	while done == False:
		# write event handlers here
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		# write game logic here
	 
		# clear the screen before drawing
		screen.fill((255, 255, 255)) 

		# write draw code here
		for slice in slices:
			segments = slice.segments
			for segment in segments + notches[slice] + flexures[slice]:
				startPoint = segment[0].copy()
				endPoint = segment[1].copy()
				startPoint.insert(slice.axisIndex(), slice.axis_position)
				endPoint.insert(slice.axisIndex(), slice.axis_position)
				pygame.draw.aaline(screen, (0,0,0), toTwoD(diff(startPoint, average), rotateX, size[0]/2, size[1]/2), 
													toTwoD(diff(endPoint, average), rotateX, size[0]/2, size[1]/2))

		# display what’s drawn. this might change.
		pygame.display.update()
		rotateX += 0.1
		# run at 60 fps
		clock.tick(60)
	 
	# close the window and quit
	pygame.quit()

def toTwoD(point, rotateX, translateX, translateY):
	transformedPoint = [
			point[0] * math.cos(rotateX) - point[1] * math.sin(rotateX),
			point[0] * math.sin(rotateX) + point[1] * math.cos(rotateX),
			-point[2]]
	return [translateX + transformedPoint[0], translateY + transformedPoint[1] + transformedPoint[2]]

def make_cuts(stlFile, svgOutput, iniParamsFile):
	params = get_params(iniParamsFile)
	
	sliceDensity = params['slice_density']
	stl_scale = params['stl_scale']
	material_thickness = params['material_thickness']
	layout_margin = params['layout_margin']
	layout_width = params['layout_width']
	flexure_to_flexure_gap = params['flexure_to_flexure_gap']
	flexure_width = params['flexure_width']
	flexure_to_edge = params['flexure_to_edge']

	print("SLICING")
	slices = slice(stlFile, sliceDensity, stl_scale)

	print("GENERATING NOTCHES")
	(notches, notchLabels) = notch(slices)
	
	print("GENERATING FLEXURES")
	flexures = flexurize(slices, material_thickness, flexure_to_flexure_gap, flexure_width, flexure_to_edge)

	print("GENERATING LAYOUT")
	offsets = layout(slices, layout_margin, layout_width)
	
	print("GENERATING SVG")
	output_svg(svgOutput, slices, notches, notchLabels, material_thickness, flexure_width, flexures, offsets)

	print("VISUALIZING")
	visualizer(slices, notches, flexures)

if len(sys.argv) != 4:
	print("Usage: python make_cuts.py stl_file_path svg_output_file_path ini_param_file_path")
else:
	stlFile = sys.argv[1]
	svgOutput = sys.argv[2]
	iniFile = sys.argv[3]
	make_cuts(stlFile, svgOutput, iniFile)

# make_cuts('stl-files/cube.stl', 'svg-files/cube.svg')
# make_cuts('stl-files/chair.stl', 'svg-files/chair.svg') # http://www.thingiverse.com/thing:141703
# make_cuts('stl-files/rhino.stl', 'svg-files/rhino.svg')
# make_cuts('stl-files/bunny.stl', 'svg-files/bunny.svg')
# make_cuts('stl-files/sphere.stl', 'svg-files/sphere.svg')
# make_cuts('stl-files/pug.stl', 'svg-files/pug.svg')
# make_cuts('stl-files/heart.stl', 'svg-files/heart.svg')