from math import sqrt
from random import randrange
from ship import Ship
from vector import distance

class Map(object):
	"""Map class that contains objects

	"""
	def __init__(self, maxPlayers):
		"""Initializes the game map
		
		@param maxPlayers: The maximum number of players the map supports
		"""
		self.origin = (0, 0)
		self.maxPlayers = maxPlayers
		self.objects = {}
		self.ships = {}

	def add_object(self, object):
		"""Adds an object to the map's global object dictionary.
		
		@param object: Object to be added to the map
		"""
		objID = id(object)
		if objID not in self.objects.keys():
			self.objects[objID] = object
			if isinstance(object, Ship):
				self.ships[objID] = object
		return objID

	def radar(self, position, range):
		"""Returns all objects within a certain radius of a position
		
		@param position: Position of the object to get radar
		@param range: Range of the radar
		"""
		return [object for object in self.objects.itervalues()
				if distance(position, object.position) <= range]
