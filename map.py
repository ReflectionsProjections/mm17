from math import sqrt
from random import randrange

class Map(object):

    def __init__(self, width, height):
        self.origin = (0, 0)
        self.width = width
        self.height = height
        self.objects = {0: self} # Mmm, hashbrowns

    @classmethod
    def add_object(self, object):
        """Adds an object to the map's global object dictionary.
        Mayne it should just be implemented as a list?"""
        id = len(self.objects) 
        self.objectts[id] = object
        return id

    @staticmethod
    def distance(pos1, pos2):
        """Returns the distance between two (x, y) position tuples"""
        return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def radar(self, position, range):
        """Returns all objects within a certain radius of a position"""
        nearby = []
        for object in self. objects:
            if distance(position, object.position) <= range:
                nearby.append(object)
        return nearby
