from vector import *

# ---------- ray casting ----------
# if there is an intersection:
# 	returns t such that
# 	origin + t * direction = intersection point on segment
# otherwise
#  	returns None
# http://stackoverflow.com/a/32146853/6153561
def ray_segment_intersect_2D(segment, origin, direction):
	AToOrigin = diff(origin, segment[0])
	AToB = diff(segment[1], segment[0])
	rayPerp = (-direction[1], direction[0])

	factor = dot(AToB, rayPerp)

	if factor == 0: # entire segment, I think. Just return none
		return None

	t1 = det_2D(AToB, AToOrigin) / factor
	t2 = dot(AToOrigin, rayPerp) / factor

	if t1 >= 0 and (t2 >= 0 and t2 <= 1):
		return t1

	return None

# cast a ray from 'origin' towards 'direction'
# will return a list of tuples (x,y) 
#  	where (x,y) is the position where the ray intersects a segment
#	ordered by distance from origin
# if no intersection is found, None is returned
def ray_cast_2D(segments, origin, direction):
	intersectionTList = []
	tSet = set()
	for segment in segments:
		t = ray_segment_intersect_2D(segment, origin, direction)
		if t is not None and t not in tSet:
			tSet.add(t)
			intersectionTList.append(t)

	if len(intersectionTList) == 0:
		return None

	intersectionTList.sort()

	intersections = []
	for t in intersectionTList:
		# origin + direction * t
		intersection = add(origin, mult(direction, t))
		intersections.append(intersection)

	return intersections

# ---- other intersection tests -----

# see if point is between the segment points
def colinear_point_on_segment(point, segmentPointA, segmentPointB):
	pointToSegA = diff(point, segmentPointA)
	pointToSegB = diff(point, segmentPointB)
	segAToSegB = diff(segmentPointA, segmentPointB)

	return dot(pointToSegA, pointToSegA) + dot(pointToSegB, pointToSegB) - dot(segAToSegB, segAToSegB) < 0.001

# return point on segment that intersects plane
# or none if none can be found
def intersect_segment_and_plane(segmentPointA, segmentPointB, planePoint, planeNormal):
	segmentDirection = diff(segmentPointB, segmentPointA)

	intersection = intersect_line_and_plane(segmentPointA, segmentDirection, planePoint, planeNormal)
	
	if intersection is None:
		return None

	if not colinear_point_on_segment(intersection, segmentPointA, segmentPointB):
		return None

	return intersection

# assuming plane is axis-aligned and lies on planeIndex axis
# returns point where the given line intersects the plane
def intersect_line_and_plane(linePoint, lineDirection, planePoint, planeNormal):
	lineToPlaneCosine = dot(lineDirection, planeNormal)

	if lineToPlaneCosine == 0:
		return None # coplanar

	lineToPlane = diff(planePoint, linePoint)
	
	factorAlongLine = dot(lineToPlane, planeNormal) / lineToPlaneCosine

	return add(linePoint, mult(lineDirection, factorAlongLine))
