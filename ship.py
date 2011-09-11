import math
import random

import Game
import Map
from vector import distance

# half of dispersion
angle_fuzz = (2*math.pi)/16

class Ship(object):
    """The class for a Player's ship.  A Player must be authorized to access certain
    methods. Any method that returns info must do so in a dictionary. """

    def __init__(self, player, position):
        self.owner = player
        self.id Game.next_id()
        self.health = 100
        self.max_thrust = 10
        self.position = position
        self.velocity = (0,0)

    def step(self, dt):
        vx, vy = self.velocity
        x, y = self.position
        self.position = (x + dt*vx, y + dt*vy)

    def thrust(self, accel):
        """ Must specify an angle. How does this tie into server? """
        dx, dx = accel
        mag = sqrt(dx*dx + dy*dy)
        if mag > self.max_accel:
            scale = self.max_accel/mag
        else:
            scale = 1
        x, y = self.velocity
        self.velocity = (x+scale*dx, y+scale*dy)

    def fire(self, angle, map):
        """Fire at angle into the ships found in the map"""
        pass

    def scan(self, ship):
        """Returns fuzzzed info if ship is in range, or None"""
        dist = distance(self.position, ship.position)
        dist_error = random.uniform(0.5,1.5)
        dist *= dist_error
        if dist < self.scan_range:
            dx = ship.position[0] - self.position[0]
            dy = ship.position[1] - self.position[1]
            if dist == 0:
                return (0,0)
            else:
                angle = math.atan2(dy,dx)
                angle_error = random.uniform(-angle_fuzz,angle_fuzz)
                angle += angle_error
                if angle < -math.pi:
                    angle += 2*math.pi
                elif angle > math.pi:
                    angle -= 2*math.pi
            return angle, dist
