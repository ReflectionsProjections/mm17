#! /usr/bin/env python

from game_obj import GameObject
import Constants

class Asteroid(GameObject):
	def __init__(self, game, position, size):
		super(Asteroid, self).__init__(game, position)
		self.size = size
		self.resources = size * Constants.asteroid_scale


	def pullResources():
		self.resources -= Constants.resource_pull

	if __name__ == '__main__':
		pass
