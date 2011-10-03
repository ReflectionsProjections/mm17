#! /usr/bin/env python
from game_instance import game
from map_obj import MapObject
import Constants
import unittest

class Asteroid(MapObject):
	"""
	An asteroid that a refinery can be built on
	"""
	def __init__(self, position, size):
		"""
		Construct an asteroid.
		
		@type  position: tuple
		@param position: Position of Asteroid on the map.
		
		@type  size: int
		@param size: Size of the Asteroid
		"""
		super(Asteroid, self).__init__(position)
		self.size = size
		self.resources = size * Constants.asteroid_scale
		self.refinery = None
		self.events = []

	def pull_resources(self):
		"""
		Remove a constant amount of resources from the asteroid.
		"""
		self.resources -= Constants.resource_pull
		if self.resources <= 0:
			if self.refinery:
				del refinery.owner.refineries[id(self)]
			self._delete()

	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return The current game state in JSON serializable representation.
		"""
		state = {'type':'asteroid',
				 'id': id(self),
				 'position': self.position,
				 'resources' : self.resources,
				 'size' : self.size,
				 'refinery' : self.refinery.to_dict if self.refinery else None
				 }
		return state

class Refinery(object):

	def __init__(self, asteroid, owner):
		"""
		Creates a refinery.
		"""
		self.asteroid = asteroid
		self.owner = owner
		self.built = 5
		self.busy = 0
		self.position = asteroid.position
		# holds all events to be processed on turn handle
		self.events = []

		# holds results from turns to be returned to user
		# dict of lists accessed like results[turn]
		self.results = {0: []}

		# set methods used to true in this dict to prevent
		# double dipping
		self.methods_used = {}

		owner.refineries[id(self)] = self


	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return The current refinery state in JSON serializable representation.
		"""
		state = { 'type':'Refinery',
				  'id': id(self),
				  'built': self.built,
				  'owner': id(self.owner),
				  'asteroid':self.asteroid.to_dict(),
				  'health':self.health,
				  'events':self.events
				  }
		return state

if __name__ == '__main__':
	unittest.main()
