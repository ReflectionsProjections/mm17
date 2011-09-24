#! /usr/bin/env python

from game_obj import GameObject
import Constants

class Asteroid(GameObject):
	def __init__(self, game, position, size):
		super(Asteroid, self).__init__(game, position)
		self.size = size
		self.resources = size * Constants.asteroid_scale
		self.refinery = None

	def pullResources():
		self.resources -= Constants.resource_pull

if __name__ == '__main__':
	unittest.main()

	def _to_dict(self):
		state = {'type':'asteroid',
				'id':id(self)
				'position': self.position
				'resources' : self.resources
				'size' : self.size
				'refinery' : id(self.refinery)}
		return state
