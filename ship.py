import math
from math import sin, cos
import random

import Game
import Map
from vector import distance, circle_in_rect

# half of dispersion
angle_fuzz = (2*math.pi)/16

class Ship(object):
	"""The class for a Player's ship.  A Player must be authorized to access certain
	methods. Any method that returns info must do so in a dictionary. """

	def __init__(self, player, position):
		self.owner = player
		self.id = Game.next_id()
		self.health = 100
		self.max_velocity = 10
		self.max_accel = 2
		self.position = position
		self.velocity = (0,0)
		self.events = []
		self.scan_range = 2000
		self.weapon_range = 1000
		self.weapon_strength = 100

	def step(self, dt):
		vx, vy = self.velocity
		x, y = self.position
		self.position = (x + dt*vx, y + dt*vy)

	def thrust(self, accel):
		""" Must specify an angle. How does this tie into server? """
		dx, dx = accel
		# test to see if the accel is greater than allowed max
		mag = sqrt(dx*dx + dy*dy)
		if mag > self.max_accel:
			scale = self.max_accel/mag
		else:
			scale = 1
		x, y = self.velocity
		self.velocity = (x+scale*dx, y+scale*dy)
		# scale doown to max velocity
		vel_mag = sqrt(self.velocity[0]**2, self.velocity[1]**2)
		vel_scale = max_velocity/vel_mag
		self.velocity = vel_scale * self.velocity
		

	def fire(self, angle):
		"""Fire at angle into the ships found in the map"""
		width = 10
		length = self.weapon_strength
		# rectangle containing laser beam.  Four points, counter clockwise
		beam = (((width/2) * sin(angle), (width/2) * -cos(angle)), #side 1
			((width/2) * sin(angle) + length * sin(angle),
			 (width/2) * -cos(angle) + length * -cos(angle)),  #side 2
			((width/2) * -sin(angle) + length * -sin(angle),
			 (width/2) * cos(angle) + length * cos(angle)),    #side 3
			((width/2) * -sin(angle), (width/2) * cos(angle))) #side 4

		within_beam = [] # list for objects in beam
		for obj in Game.game_map.objects:
			if circle_in_rect(beam, obj.position, obj.radius):
				within_beam.append(obj)
		
		if len(within_beam) == 0:
			# No object hit
			self.events.append(("shot", None))
		else:
			within_beam.sort(key=distance(self.position, obj.position))
			# Hit first in line, record id
			self.events.append(("shot", within_beam[0].id))
			# register damage with hit object
			dist = distance(self.position, within_beam[0].position)
			damage_amt = self.weapon_strength *(self.weapon_range - \
								    dist)/weapon_range 
			within_beam[0].events(("damage", self.id, damage_amt)
					   

	def scan(self, ship):
		"""Returns fuzzzed info if ship is in range, or None"""
		# Multiply the returned distance by a random value
		dist = distance(self.position, ship.position)
		if dist < self.scan_range:
			dist_error = random.uniform(0.5,1.5)
			dist *= dist_error
			dx = ship.position[0] - self.position[0]
			dy = ship.position[1] - self.position[1]
			if dist == 0:
				return (0,0)
			else:
				angle = math.atan2(dy,dx)
				angle_error = random.uniform(-angle_fuzz,angle_fuzz)
				angle += angle_error
				if angle < -math.pi:
					angle += 2*math.pi
				elif angle > math.pi:
					angle -= 2*math.pi
			return angle, dist, ship.health
		else: return None
