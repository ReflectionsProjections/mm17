#! /usr/bin/env python

from math import sin, cos, sqrt, pi, hypot, atan2
import random
import Constants

from game_obj import GameObject
from vector import distance, circle_in_rect

# half of dispersion
angle_fuzz = (2*pi)/16

class Ship(GameObject):
	"""The class for a Player's ship.  A Player must be authorized to access
	certain methods. Any method that returns info must do so in a dictionary.
	"""

	def __init__(self, game, position, owner):
		super(Ship, self).__init__(game, position)
		"""Add a ship to the game.

		@param game: The game to add the ship to
		@param position: The position to locate the ship
		@param owner: The player that is creating this ship
		"""
		self.size = Constants.base_size
		self.direction = 0
		self.owner = owner
		self.alive = True
		# attribute itialization
		self.health = Constants.base_health
		self.scan_range = Constants.scan_range
		self.weapon_range = Constants.weapon_range
		self.weapon_strength = Constants.weapon_strength
		# max values
		self.max_velocity = Constants.max_velocity
		self.max_accel = Constants.max_accel
		self.methods_used = {'thrust':False,'fire':False}

	def thrust(self, accel):
		"""Sets the velocity based on acceleration and current velocity.

		@param accel: (x,y) acceleration tuple
		"""
		# test to see if the accel is greater than allowed max
		mag = hypot(*accel)
		if mag > self.max_accel:
			scale = self.max_accel/mag
		else:
			scale = 1
		x, y = self.velocity
		dx, dy = accel
		self.velocity = (x+scale*dx, y+scale*dy)
		# scale doown to max velocity
		vel_mag = hypot(*self.velocity)
		vel_scale = self.max_velocity/vel_mag
		self.velocity = (vel_scale * self.velocity[0],
				vel_scale * self.velocity[1])
		# XXX: What the fuck was this supposed to do
		#self.direction =

	def fire(self, angle):
		"""Fire at angle relative to the ship's direction.  The laser is
		instant and is a rectangle with a width of 10 and a length of
		self.weapon_strength. Any object that intersects that rectatngle
		takes damage.

		@param angle: angle relative to ships direction as radians
		"""
		width = 10
		length = self.weapon_strength

		#angle is relative to ship's direction
		angle += self.angle

		w = width/2
		# Four points, counter clockwise
		p_0 = (self.position[0] + w * cos(angle),
				self.position + w * -sin(angle))
		p_3 = (self.position[0] + w * -cos(angle),
				self.position + w * sin(angle))
		p_1 = (p_0[0] + length * cos(angle), p_0[1] + length * sin(angle))
		p_2 = (p_1[0] + length * cos(angle), p_1[1] + length * sin(angle))

		# rectangle of laser beam
		beam = (p_0, p_1, p_2, p_3)

		within_beam = [] # list for objects in beam
		for obj in self.game.game_map.objects:
			if circle_in_rect(beam, obj.position, obj.radius):
				within_beam.append(obj)

		if len(within_beam) == 0:
			# No object hit
			self.events.append(("shot", None))
		else:
			within_beam.sort(key=distance(self.position, obj.position))
			# Hit first in line, record id
			self.events.append(("shot", id(within_beam[0])))
			# register damage with hit object
			dist = distance(self.position, within_beam[0].position)
			damage_amt = self.weapon_strength *(self.weapon_range - \
					dist)/weapon_range
			within_beam[0].events.append({'type':'damage',
					'amount':damage_amt,
					'hit_by':id(self)})

	def scan(self, object):
		"""Scan an object, the data is fuzzed based on distance from the ship

		@param: The object to get fuzzed data from
		@return: The fuzzed angle and distance
		"""
		# Multiply the returned distance by a random value
		dist = distance(self.position, object.position)
		if dist < self.scan_range:
			dist_error = random.uniform(0.5,1.5)
			dist *= dist_error
			dx = object.position[0] - self.position[0]
			dy = object.position[1] - self.position[1]
			if dist == 0:
				return angle, dist
			else:
				angle = atan2(dy, dx)
				angle_error = random.uniform(-angle_fuzz,angle_fuzz)
				angle += angle_error
				if angle < -pi:
					angle += 2*pi
				elif angle > pi:
					angle -= 2*pi
				return angle, dist
		else:
			return None

	def create_ship(self):
		"""Temporary method to create a ship near another ship"""
		new_ship = Ship(self.game, self, (self.position+5,
				self.position+5))
		self.game.game_map.add_object(new_ship)
		self.add_object(new_ship)

	def _to_dict(self):
		state = {'type':'ship',
			'id':id(self),
			'owner': self.owner.name,
			'alive': self.alive,
			'position': self.position,
			'velocity': self.velocity,
			'health': self.health}
		return state

if __name__ == '__main__':
	unittest.main()
