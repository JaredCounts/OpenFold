class Slice(object):
	def __init__(self):
		self.axis = (1,0,0)
		self.axis_position = 0
		self.segments = []

	# get index of axis this slice is perpendicular to
	# eg, if it is perpendicular to (0,1,0), 
	# 	then 1 is returned since the y axis is at index 1
	def axisIndex(self):
		index = 0
		if self.axis[0] != 0:
			index = 0
		elif self.axis[1] != 0:
			index = 1
		else:
			assert self.axis[2] != 0
			index = 2
		return index


def slice(file):
	pass