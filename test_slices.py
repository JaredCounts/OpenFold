from slicer import *

# generate slices for a test box
def test_box():
	slice1 = Slice()
	slice1.axis = 'x'
	slice1.axis_position = 0.25
	slice1.segments = [( (0,0), (1,0) ),
					   ( (1,0), (1,1) ),
					   ( (1,1), (0,1) ),
					   ( (0,1), (0,0) )]
	slice2 = Slice()
	slice2.axis = 'x'
	slice2.axis_position = 0.75
	slice2.segments = [( (0,0), (1,0) ),
					   ( (1,0), (1,1) ),
					   ( (1,1), (0,1) ),
					   ( (0,1), (0,0) )]

	slice3 = Slice()
	slice3.axis = 'z'
	slice3.axis_position = 0.25
	slice3.segments = [( (0,0), (1,0) ),
					   ( (1,0), (1,1) ),
					   ( (1,1), (0,1) ),
					   ( (0,1), (0,0) )]
	slice4 = Slice()
	slice4.axis = 'z'
	slice4.axis_position = 0.75
	slice4.segments = [( (0,0), (1,0) ),
					   ( (1,0), (1,1) ),
					   ( (1,1), (0,1) ),
					   ( (0,1), (0,0) )]

	return [slice1, slice2, slice3, slice4]
