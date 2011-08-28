import Player
import Map

class Ship(object):
    def __init__(self, Player, position):
        self.owner = Player
        self.id = Player.nextId
        self.level = 1
        self.talents = {'weapons': 1, 'shields': 1, 'speed': 1}
        self.position = position
        
    def scan(self, ship = self)

    def move(self, angle):
        self.direction = angle

    class Laser(object):
        def __init__(self, ship, origin, angle, range):
            self.ship = ship
            self.direction = angle
            self.origin = origin


    def shoot(self, angle):
        Map.fired_shots.append(Laser(self, self.position, angle, range)) 
