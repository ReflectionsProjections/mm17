class Player(object):
    def __init__(self, name, color, id):
        self.name = name
        self.color = color
        self.id = id
        self.planets = []
        self.ships = []
