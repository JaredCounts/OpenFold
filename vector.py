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