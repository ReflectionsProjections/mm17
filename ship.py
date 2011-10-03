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
		self.max_accel = Constants.max_accel
		self.max_velocity = Constants.max_velocity
		self.methods_used = {'thrust':False,
							 'fire':False,
							 'create_base':False,
							 'create_refinery':False,
							 'scan':False}
		owner.add_object(self)


	def thrust(self, direction, speed):
		"""Sets the velocity based on acceleration and current velocity.

		@param accel: (x,y) acceleration tuple
		"""
		# test to see if the accel is greater than allowed max
		mag = hypot(*direction)
		x, y = self.velocity
		if mag != 0:
			dx, dy = (direction[0]/mag, direction[1]/mag)
		else:
			dx, dy = (0, 0)
		scale = self.max_accel if speed > self.max_accel else speed
		self.velocity = (x + scale*dx, y + scale*dy)
		# scale doown to max velocity
		vel_mag = hypot(*self.velocity)
		if vel_mag >= self.max_velocity:
			vel_scale = self.max_velocity/vel_mag
		else: vel_scale = 1
		self.velocity = (vel_scale * self.velocity[0],
						 vel_scale * self.velocity[1])
		self.direction = atan2(*direction)

	def fire(self, direction):
		from game_instance import game
		"""Fire at angle relative to the ship's direction.  The laser is
		instant and is a rectangle with a width of 10 and a length of
		self.weapon_strength. Any object that intersects that rectatngle
		takes damage.

		@param direction: vector to fire at 
		"""
		width = Constants.weapon_width
		length = self.weapon_range
		mag = hypot(*direction)
		if mag != 0:
			normalized = (direction[0]*(length/mag),direction[1]*(length/mag))
		else: normalized = (0,0)
		angle = atan2(*direction)
		w = width/2
		# Four points, counter clockwise
		p_0 = (self.position[0] + w * cos(angle),
				self.position[1] + w * -sin(angle))
		p_3 = (self.position[0] + w * -cos(angle),
				self.position[1] + w * sin(angle))
		p_1 = (p_0[0] + length * sin(angle), p_0[1] + length * cos(angle))
		p_2 = (p_3[0] + length * sin(angle), p_3[1] + length * cos(angle))

		# rectangle of laser beam
		beam = (p_0, p_1, p_2, p_3)
		within_beam = [] # list for objects in beam
		for obj in game.game_map.objects.itervalues():
			hit = circle_in_rect((obj.position, obj.size), beam)
			if hit and obj != self:
				if hasattr(obj,'alive'):
					if obj.alive: within_beam.append(obj)
				else:
					within_beam.append(obj)
		if len(within_beam) == 0:
			# No object hit
			self.events.append({'type':'shot','hit': None})
		else:
			cmp_dist = lambda a: distance(self.position, a.position)
			within_beam.sort(key=cmp_dist)
			# Hit first in line, record id
			hit = within_beam[0]
			if hasattr(hit, 'base') and hit.base != None:
				hit = hit.base
			if hasattr(hit, 'refinery') and hit.base != None:
				hit = hit.refinery
			self.events.append({'type':'shot', 'hit': id(hit),'obj_type':hit.__class__.__name__})
			# register damage with hit object
			diagonal = distance(self.position, p_2)
			dist = distance(self.position, hit.position)
			damage_amt = Constants.weapon_strength
			hit.events.append({'type':'damage',
										  'amount':damage_amt,
										  'hit_by':id(self)})
		with game.lasers_shot_lock:
			game.lasers_shot[game.turn].append({'start': self.position, 
												'direction':normalized})

	def scan(self, object):
		"""Scan an object, the data is fuzzed based on distance from the ship

		@param object: The object to get fuzzed data from
		"""
		# Multiply the returned distance by a random value
		dist = distance(self.position, object.position)
		angle = hypot(*object.position)
		dist_error = random.uniform(0.5,1.5)
		dist *= dist_error
		dx = object.position[0] - self.position[0]
		dy = object.position[1] - self.position[1]
		if dist == 0:
			return angle, dist
		else:
			angle = atan2(dy, dx)
			angle_error = random.uniform(-angle_fuzz, angle_fuzz)
			angle += angle_error
			if angle < -pi:
				angle += 2*pi
			elif angle > pi:
				angle -= 2*pi
				return {'angle':angle, 'distance':dist}
			

	def to_dict(self):
		"""
		Returns dict that can be used by JSON
		"""
		state = {'type':'ship',
				 'id':id(self),
				 'owner': id(self.owner),
				 'alive': self.alive,
				 'position': self.position,
				 'velocity': self.velocity,
				 'direction': self.direction,
				 'health': self.health,
				 'size': self.size,
				 'events':self.events
				 }
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

	def create_base(self, planet):
		"""
		Create a base on a planet

		@type planet: Planet object
		@param planet: Planet to build your base on
		"""
		new_base = Base(planet, self.owner)
		resources -= Constants.base_price
		return new_base

class TestShip(unittest.TestCase):
	pass


if __name__ == '__main__':
	unittest.main()
