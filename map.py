from math import sqrt
from random import randrange

class Map:

    def __init__(self, width, height):
        self.origin = (0, 0)
        self.width = width
        self.height = height
        self.objects = {} # Mmm, hashbrowns

    def add_object(self, object, point):
        """ Adds a dictionary entry to Map.objects containing 
        the (obj_x, obj_y, radius) tuple """
        if isinstance(point, tuple):
            self.objects[object] = point
        else:
            raise Exception("Must submit location as a tuple!")

    def radar(self, location, radius):
        """ Looks to see if any objects are within the radius
        of the radar and returns a list of (object, (obj_x, obj_y))
        tuples. """
        nearby = []
        for object, position in self.objects:
            delta_x = location[0] - position[0]
            delta_y = location[1] - position[1]
            distance = sqrt(delta_x**2 + delta_y**2)
            if distance <= radius / 2:
                nearby.append((object, position))
            elif distance >= radius / 2 && distance <= radius:
                # Screw with your radar!  Random floating point
                # multiplication.  NEEDS TESTING
                position = tuple([x.randrange(0.6, 1.0) for x in position])
                nearby.append((object, position))
            else: pass
        return nearby

 
