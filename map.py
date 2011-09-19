from math import sqrt
from random import randrange

from vector import distance

class Map(object):

	def __init__(self, width, height, maxPlayers):
		self.origin = (0, 0)
		self.width = width
		self.height = height
		self.maxPlayers = maxPlayers
		self.objects = {} # Mmm, hashbrowns

	def add_object(self, object):
		"""Adds an object to the map's global object dictionary.
		Mayne it should just be implemented as a list?"""

		objID = id(object)
		if objID not in self.objects:
			self.objects[objID] = object

		return objID

	def radar(self, position, range):
		"""Returns all objects within a certain radius of a position"""
		return [object for object in self.objects.itervalues()
				if distance(position, object.position) <= range]
