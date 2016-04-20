from Slice import *

def slice(file):
    """
    input: file -> string file path to stl
    output: list of Slice, s.t.
        Slice.axis = 
            (1,0,0) if perpendicular to x axis or
            (0,1,0) if perpendicular to y axis or
            (0,0,1) if perpendicular to z axis
        Slice.axis_position = distance along Slice.axis from origin in stl file
        Slice.segments = list of segments, such that
            Each segment is a tuple of coordinates such that
            Each coordinate is a tuple of floats
            Eg. if axis is ‘x’, then they’re (y,z) coordinates
            Ie. [((a,b), (c,d)), ...]
    """



	pass