import Game
import Map

class Ship(object):
    """The class for a Player's ship.  Access to ship methods is through
    /ship/{id}/{method}.  A Player must be authorized to access certain
    methods. Any method that returns info must do so in a dictionary. """

    def __init__(self, player, position):
        self.owner = player
        self.id Game.next_id()
        self.level = 1
        self.experience = 0
        self.health = 100
        self.talents = {'weapons': 1, 'shields': 1, 
                        'speed': 1, 'radar': 1}
        self.talent_points = 0
        self.position = position
        self._update_attrs(self.talents)
        return (200)

    def info(self):
        """ GET method.  Must provide auth token for some info?  Also, 
        scan method accesses this if the other ship is within range. """
        info = {'id' : self.id, 
                'owner' : self.id,
                'position' : self.position,
                'level' : self.level,
                'talents' : self.talents,
                'experience' : self.experience,
                'health' : self.health,
                }
        return (200, info)

    def move(self, angle):
        """ POST method.  Must specify an angle. How does this tie into server? """
        self.direction = angle
        return (200)

    class Laser(object):
        """ The Laser class!  Defines a shot. """
        def __init__(self, ship, origin, angle):
            self.ship = ship
            self.direction = angle
            self.origin = ship.position
            self.range = ship.weapon_range


    def shoot(self, angle):
        """ POST method, must define an angle. Creates a new LAser blast and registers it with the Map. """
        shot = self.Laser(self, self.position, angle, self.weapon_range)
        return (200, shot)

    def scan(self, ship_id):
        """ POST method.  Scans a ship if in range and returns ship.info.  Otherwise it raises a RangeException. """
        if distance(self.position, ship.position) < self.scan_range:
            return (200, ship.info())
        else:
            return (403, "Ship" + ship_id + "is out of range!"}

    def _update_attrs(self):
        """ Internal method that updates attributes after a talent boost. """
        ranges = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900,
                  1000, 1100, 1200, 1300, 1400, 1500, 1600]

        self.radar_range = ranges[self.talents['radar']]
        self.scan_range = ranges[self.talents['radar'] / 5]
        self.weapon_power = ranges[self.talents['weapons'] / 10]
        self.weapon_range = ranges[self.talents['weapons'] / 5]
        self.shield_strength = ranges[self.talents['shields'] / 5]
        self.speed = ranges[self.talents['speed'] / 10]

    def add_talent_point(self, talent_str):
        """ POST method to increment a talent tree by one point. """
        if self.talent_points > 0:
            self.talents[talent_str] += 1
            self.talent_points -= 1
            self._update_attrs()
            return (200)
        else:
            return (400,  "Not enough points!")
        
    def radar(self):
        """ GET method.  Returns a list of 'blips' with some info based
        on position and radar range. """
        return (200, Map.radar(self.position, self.radar_range))
                         
 
