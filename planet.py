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

	def _to_dict(self):
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

class Base(object):
	"""
	A base that can be built on a planet.  Players can use these to
	create ships, etc.
	"""

	def __init___(self, planet, owner):
		"""
		Construct a base.

		@type planet: Planet object
		@param planet: The Planet object that this base is associated with
		
		@type owner: Player object
		@param owner: The Player object this base is owned by
		"""
		self.planet = planet
		self.owner = owner
		self.health = Constants.base_health

	def create_ship(self, position):
		"""
		Construct a ship.
		
		@type: tuple
		@param position: location the player wants the object at
		"""
		# if outside build radius, move position in
		if distance(self.planet.position, position) > Constants.build_radius:
			mag = hypot(*position)
			position = (position[0]*(build_radius/mag),
						position[1]*(build_radius/mag))
		new_ship = Ship(position, self.planet.owner)
		return new_ship

	def salvage_ship(self, ship):
		"""
		Salvage a ship, reimbursin you with 0-50% of your resources.

		@type ship: Ship object
		@param ship: A ship object to delete within the salvage_radius
		"""
		resources = (ship.health/ Contstanst.ship_health)*\
			(Constants.ship_price / 2)
		ship._delete()
		self.owner.resources += resources


if __name__ == '__main__':
	unittest.main()
