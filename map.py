from math import sqrt
from random import randrange

from vector import distance

class Map(object):

	def __init__(self, maxPlayers):
		self.origin = (0, 0)
		self.maxPlayers = maxPlayers
		self.objects = {}
		self.ships = {}

	def add_object(self, object):
		"""Adds an object to the map's global object dictionary."""
		objID = id(object)
		if objID not in self.objects.keys():
			self.objects[objID] = object
			if isinstance(object, Ship):
				self.ships[objID] = object
		return objID

	def radar(self, position, range):
		"""Returns all objects within a certain radius of a position"""
		return [object for object in self.objects.itervalues()
				if distance(position, object.position) <= range]
