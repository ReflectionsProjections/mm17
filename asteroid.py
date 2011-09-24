#! /usr/bin/env python

from map_obj import MapObject
import Constants

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
		super(Asteroid, self).__init__(game, position)
		self.size = size
		self.resources = size * Constants.asteroid_scale
		self.refinery = None

	def pull_resources(self):
		"""
		Remove a constant amount of resources from the asteroid.
		"""
		self.resources -= Constants.resource_pull

if __name__ == '__main__':
	unittest.main()

	def _to_dict(self):
		state = {'type':'asteroid',
					'id': id(self),
					'position': self.position,
					'resources' : self.resources,
					'size' : self.size,
					'refinery' : id(self.refinery)}
		return state

class Refinery(object):
	def __init__(self, game, asteroid, owner)
	self.game = game
	self.asteroid = asteroid
	self.owner = owner


	def _to_dict(self)

		state = { 'type':'Refinery'
					'id':id(self)
					'asteroid':self.asteroid}
		return state
