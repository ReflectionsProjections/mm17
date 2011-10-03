#! /usr/bin/env python

import unittest
from vector import distance
import Constants
from map_obj import MapObject
from ship import Ship
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
		super(Planet, self).__init__(position)

		self.size = size
		# will contain refrence to base if it contains one
		self.base = None

	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return The current game state in JSON serializable representation.
		"""
		state = {'type': 'Planet',
				 'id': id(self),
				 'position': self.position,
				 'size':self.size,
				 'base': id(self.base) if self.base else 0
				}
		return state

class Base(object):
	"""
	A base that can be built on a planet.  Players can use these to
	create ships, etc.
	"""

	def __init__(self, planet, owner):
		"""
		Construct a base.

		@type planet: Planet object
		@param planet: The Planet object that this base is associated with
		
		@type owner: Player object
		@param owner: The Player object this base is owned by
		"""
		self.built = 10
		self.alive = True
		self.planet = planet
		self.owner = owner
		self.position = self.planet.position
		self.health = Constants.base_health
		self.events = []
		self.busy = 0
		owner.add_object(self)
		self.planet.base = self
		# holds all events to be processed on turn handle
		self.events = []

		# holds results from turns to be returned to user
		# dict of lists accessed like results[turn]
		self.results = {0: []}

		# set methods used to true in this dict to prevent
		# double dipping
		self.methods_used = {}

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
		self.planet.owner.resources -= Constants.ship_price
		return new_ship

	def salvage_ship(self, ship):
		"""
		Salvage a ship, reimbursin you with 0-50% of your resources.

		@type ship: Ship object
		@param ship: A ship object to delete within the salvage_radius
		"""
		resources = (ship.health/ Contstanst.base_health)*\
			(Constants.ship_price / 2)
		ship._delete()
		self.owner.resources += resources

	def repair_ship(self, ship):
		"""
		Repair a ship, adding repair_percent ship health per turn used.
		
		@type ship: Ship object
		@param ship: A ship object to add health to
		"""
		ship.health += Constants.repair_percent * Constants.base_health
		if ship.health > Constants.base_health:
			ship.health = Constants.base_health

	def destroy(self):
		"""
		Removes a base from the planet and owner refrences
		"""
		self.alive = False
		self.planet.base = None


	def to_dict(self):
		"""
		Return the current state in JSON serializable representation.

		@type: dict
		@return: The current base state in JSON serializable representation.
		"""
		state = { 'type':'Base',
				  'id': id(self),
				  'built': self.built,
				  'position': self.position,
				  'planet':self.planet.to_dict(),
				  'owner': id(self.owner),
				  'health': self.health,
				  'events':self.events
				  }
		return state

	
if __name__ == '__main__':
	unittest.main()
