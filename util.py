# ---------- Vector stuff ----------
# http://stackoverflow.com/questions/1984799/cross-product-of-two-vectors-in-python
def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    return c

def dot(a,b):
	assert len(a) == len(b)

	dot = 0
	for i in range(0, len(a)):
		dot += a[i] * b[i]

	return dot

# returns a + b
def add(a,b):
	assert len(a) == len(b)

	c = []
	for i in range(0, len(a)):
		c.append(a[i] + b[i])
	return c

# returns b - a
def diff(b,a):
	assert len(a) == len(b)

	c = []
	for i in range(0, len(a)):
		c.append(b[i] - a[i])

	return c

# the determinant between two 2d vectors
def det_2D(a,b):
	return a[0] * b[1] - a[1] * b[0]

# return a multiplied by some scalar
def mult(a, scalar):
	c = []
	for coeff in a:
		c.append(coeff * scalar)
	return c

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
	for segment in segments:
		t = ray_segment_intersect_2D(segment, origin, direction)
		if t is not None:
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
