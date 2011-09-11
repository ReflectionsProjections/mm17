from math import sqrt
from random import randrange

from vector import distance

class Map(object):

    def __init__(self, width, height):
        self.origin = (0, 0)
        self.width = width
        self.height = height
        self.objects = {} # Mmm, hashbrowns

    def add_object(self, object):
        """Adds an object to the map's global object dictionary.
        Mayne it should just be implemented as a list?"""
        id = len(self.objects)
        object.id = id
        self.objectts[id] = object
        return id

    def radar(self, position, range):
        """Returns all objects within a certain radius of a position"""
        return [object for object in self.objects.itervalues()
                if distance(position, object.position) <= range]
