from math import fabs

def distance(pos1, pos2):
	"""Returns the distance between two (x, y) position tuples"""
	return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def intersect_circle(center, radius, line):
	""" Checks to see if a line intersects with a circle.
	center = (x,y) coordinate of circle center
	radius = radius of circle
	line = ((x, y), (x,y)) start and end points of line

	returns True/False"""

	line_v = line[1][0]-line[0][0], line[0][1]-line[0][1]           # Vector of line
        line_len = sqrt(line_v[0]**2 + line_v[1]**2)         # Length of line
	line_v = line_v[0]/line_len, line_v[1]/line_len               # unit vector of line
	normal = -line_v[1], line_v[0]                    # normal unit vector
        center_line_v = center[0]-line[1][0], center[1]-line[1][1] # vector from point to end
	dist = fabs(ac[0]*n[0]+ac[1]*n[1]) # Projection of center_line_v to n (the minimum distance)
	if dist < radius: return True
	else: return False


def circle_in_rect(rect, center, radius):
	""" Checks to see if a circle intersects the rectangle.
	Also returns true if center is in rectangle.
	rect should be a tuple of fours points, stored CCW
	point should be an x,y coordinate
	"""

	# each side has a start point and a vector
	sides = [(rect[0], (rect[1][0] - rect[0][0], rect[1][1] - rect[0][1])),
		 (rect[1], (rect[2][0] - rect[1][0], rect[2][1] - rect[1][1])),
		 (rect[2], (rect[3][0] - rect[2][0], rect[3][1] - rect[2][1])),
		 (rect[3], (rect[0][0] - rect[3][0], rect[0][1] - rect[3][1]))]

	center_right_of_side = 0 # must be four to be true
	for side in sides:
		# find vector bewtween point and start of side
		vector = (side[0][0] - center[0], siode[0][1] - center[1])
		# take cross product between vector and side
		cross_prod = side[1][0]*vector[1] - side[1][1]*vector[0]
		# if side intersects ciclre, return true
		if intersect_circle(center, radius, side[1]):
			return True
		# if the following is true for all sides, center is in rect
		if cross_prod > 0:
			center_right_of_side+=1
	# if we have 4, then circle is in rect
	if center_right_of_side == 4:
		return True
	else:
		return False



def circle_collision(circle1, circle2):
	""" Checks to see if a line intersects with a circle.
	circle = ((x,y), radius) center and radius

	returns True/False"""
	if circle1[1] > circle2[1]:
		bigger = circle1
	else: bigger = circle2
	dist = distance(circle1[0], circle2[0])
	if dist < bigger[1]: return True
	else: return False
