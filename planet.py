#! /usr/bin/env python

from map_obj import MapObject
import Constants
import unittest

class Planet(MapObject):
	"""
	A planet that can be captured. A base can be built here by a ship.
	"""

	def __init__(self, position, size):
		"""
		Construct a planet.

		@type  position: tuple
		@param position: Position of Planet on the map
		
		@type  size: int
		@param size: Size of the Planet
		"""
		super(Planet, self).__init__(game, position)
		
		self.size = Constantse
		self.resources = size * Constants.planet_scale
		# will contain refrence to base if it contains one
		self.base = None

	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return The current game state in JSON serializable representation.
		"""
		state = {
				'obj_id': id(self),
				'position': self.position,
				'base': id(self.base) if self.base else None
				}
		return state

if __name__ == '__main__':
	unittest.main()
