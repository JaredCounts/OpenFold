from vector import *
import pygame
import math
 
def visualizer(slices, notches, flexures):
	average = [0,0,0]
	pointCount = 0
	minimum = [9999,9999,9999]
	maximum = [-9999,-9999,-9999]
	for slice in slices:
		for segment in slice.segments:
			startPoint = segment[0].copy()
			endPoint = segment[1].copy()
			startPoint.insert(slice.axisIndex(), slice.axis_position)
			endPoint.insert(slice.axisIndex(), slice.axis_position)
			average = add(average, startPoint)
			average = add(average, endPoint)
			for i in range(0, 3):
				minimum[i] = min(minimum[i], startPoint[i])
				maximum[i] = max(maximum[i], startPoint[i])
				minimum[i] = min(minimum[i], endPoint[i])
				maximum[i] = max(maximum[i], endPoint[i])
			pointCount += 2

	mesh_range = diff(maximum, minimum)
	max_range = max(mesh_range)
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
	rotateY = 0
	scale = 1

	resize = min(size) / max_range * 0.75

	# Loop until the user clicks close button
	done = False
	while done == False:
		# write event handlers here
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					scale *= 1.15
				if event.button == 5:
					scale *= 0.85
			if event.type == pygame.MOUSEMOTION:
				if event.buttons[0]:
					pos = event.rel
					rotateX -= pos[0] * 0.01
					rotateY += pos[1] * 0.01
	 
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
				pygame.draw.aaline(screen, (0,0,0), toTwoD(mult(diff(startPoint, average), resize * scale), rotateX, rotateY, size[0]/2, size[1]/2), 
													toTwoD(mult(diff(endPoint, average), resize * scale), rotateX, rotateY, size[0]/2, size[1]/2))

		# display what’s drawn. this might change.
		pygame.display.update()
		# rotateX += 0.1
		# run at 60 fps
		clock.tick(60)
	 
	# close the window and quit
	pygame.quit()

def toTwoD(point, rotateX, rotateY, translateX, translateY):
	transformedPoint = [
			point[0] * math.cos(rotateX) - point[1] * math.sin(rotateX),
			point[0] * math.sin(rotateX) + point[1] * math.cos(rotateX),
			-point[2]]
	transformedPoint = [
			transformedPoint[0],
			transformedPoint[1] * math.cos(rotateY) - transformedPoint[2] * math.sin(rotateY),
			transformedPoint[1] * math.sin(rotateY) + transformedPoint[2] * math.cos(rotateY)
		]
	return [translateX + transformedPoint[0], translateY + transformedPoint[1] + transformedPoint[2]]
