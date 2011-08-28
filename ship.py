from Game import RangeException, Map, Player

class Ship(object):
    def __init__(self, Player, position):
        self.owner = Player
        self.id = Player.nextId
        self.level = 1
        self.experience = 0
        self.health = 100
        self.talents = {'weapons': 1, 'shields': 1, 
                        'speed': 1, 'radar': 1}
        self.position = position
        self.update_attrs(self.talents)

    def info(self):
        info = {'id' : self.id,
                'owner' : self.id,
                'position' : self.position,
                'level' : self.level,
                'talents' : self.talents,
                'experience' : self.experience,
                'health' : self.health,
                }
        return info

    def move(self, angle):
        self.direction = angle

    class Laser(object):
        def __init__(self, ship, origin, angle, range):
            self.ship = ship
            self.direction = angle
            self.origin = origin


    def shoot(self, angle):
        shot = self.Laser(self, self.position, angle, range)
        Map.fired_shots.append(shot)

    def scan(self, ship):
        if distance(self.position, ship.position) < self.scan_range:
            return ship.info()
        else:
            raise RangeException()

    def update_attrs(self):
        ranges = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900,
                  1000, 1100, 1200, 1300, 1400, 1500]
        self.radar_range = ranges[self.talents['radar']]
        self.scan_range = ranges[self.talents['radar'] / 5]
        self.weapon_power = ranges[self.talents['weapons'] / 10]
        self.shield_strength = ranges[self.talents['shields'] / 5]
        self.speed = ranges[self.talents['speed'] / 10]

    def add_talent_point(self, talent_str):
        self.talents[talent_str] += 1
        self.update_attrs()
        
    def radar(self):
        return Map.radar(self.position, self.radar_range)
                         
