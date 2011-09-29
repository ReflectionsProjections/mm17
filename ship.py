#! /usr/bin/env python

from math import sin, cos, sqrt, pi, hypot, atan2
import unittest
import random
import Constants
from player import Player
from map_obj import MapObject
from vector import distance, circle_in_rect

# half of dispersion
angle_fuzz = (2*pi)/16

class Ship(MapObject):
	"""The class for a Player's ship.  A Player must be authorized to access
	certain methods. Any method that returns info must do so in a dictionary.
	"""

	def __init__(self, position, owner):
		super(Ship, self).__init__(position)
		"""Add a ship to the game.

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

	def fire(self, angle):
		from game_instance import game
		"""Fire at angle relative to the ship's direction.  The laser is
		instant and is a rectangle with a width of 10 and a length of
		self.weapon_strength. Any object that intersects that rectatngle
		takes damage.

		@param angle: angle relative to ships direction as radians
		"""
		width = 10
		length = self.weapon_strength

		#angle is relative to ship's direction
		angle += self.direction

		w = width/2
		# Four points, counter clockwise
		p_0 = (self.position[0] + w * cos(angle),
				self.position[1] + w * -sin(angle))
		p_3 = (self.position[0] + w * -cos(angle),
				self.position[1] + w * sin(angle))
		p_1 = (p_0[0] + length * cos(angle), p_0[1] + length * sin(angle))
		p_2 = (p_1[0] + length * cos(angle), p_1[1] + length * sin(angle))

		# rectangle of laser beam
		beam = (p_0, p_1, p_2, p_3)

		within_beam = [] # list for objects in beam
		for obj in game.game_map.objects.itervalues():
			if circle_in_rect(obj.position, obj.size, beam):
				within_beam.append(obj)

		if len(within_beam) == 0:
			# No object hit
			self.events.append(("shot", None))
		else:
			cmp_dist = lambda a: distance(self.position, a.position)
			within_beam.sort(key=cmp_dist)
			# Hit first in line, record id
			self.events.append(("shot", id(within_beam[0])))
			# register damage with hit object
			dist = distance(self.position, within_beam[0].position)
			damage_amt = Constants.weapon_strength *(Constants.weapon_range - \
					dist)/Constants.weapon_range
			within_beam[0].events.append({'type':'damage',
					'amount':damage_amt,
					'hit_by':id(self)})

	def scan(self, object):
		"""Scan an object, the data is fuzzed based on distance from the ship

		@param object: The object to get fuzzed data from
		"""
		# Multiply the returned distance by a random value
		dist = distance(self.position, object.position)
		angle = hypot(*object.position)
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

	def to_dict(self):
		"""
		Returns dict that can be used by JSON
		"""
		state = {'type':'ship',
				 'id':id(self),
				 'owner': self.owner.name,
				 'alive': self.alive,
				 'position': self.position,
				 'velocity': self.velocity,
				 'health': self.health}
		return state

	def create_refinery(self, asteroid):
		"""
		Create a refinery on an asteroid

		@type asteroid: Asteroid object
		@param asteroid: Asteroid to build refinery on
		"""
		new_refinery = Refinery(asteroid, self.owner)
		resources -= Constants.refinery_price
		return nee_refinery

class TestShip(unittest.TestCase):
	def setUp(self):
		from game_map import Map
		from game import Game
		self.game_map = Map(1)
		self.game = Game(self.game_map,"test_log")
		self.player = self.game.add_player("test","auth")

	def test_create(self):
		self.ship = Ship((1,2),self.player)
		self.assertEquals(self.ship.position, (1,2))
		self.assertEquals(self.ship.health, Constants.base_health)


	def tearDown(self):
		self.game.active = False
		# thread should eventually kill itself, if it is running
		del self.ship
		del self.player
		del self.game_map
		del self.game



if __name__ == '__main__':
	unittest.main()
