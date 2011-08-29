import datetime
import Player

class Game:
    """The main Game class runs the game and contains the main loop
    that updates statuses and logs data."""

    def __init__(self, map, log_file):
        self.players = []
        self.map = map
        self.log_file = log_file
        self.next_id

    def _log(self, message):
        """ Adds a message to the end of the log file. """
        with open(self.log_file, 'a') as log:
            text = "%s: %s" % (datetime.now, message)
            log.write(text)

    def _begin(self):
        self.active = True
        self.start_time = datetime.now
        self._log("Game started.")
        
    def _end(self):
        self._log("Game ended.")
        self.active = False

    def _add_player(self, name, color):
        new = Player(name, id = len(self,players), color)
        self.players.append(Player)
    
    def _check_players(self):
        actives = [player for player in self.players if player.active == True]
        if len(actives) > 1: return True
        else: return False

    def _main(self):
        while self.active == True:
            if _check_players == False: self._end

    def next_id(self):
        self.next_id += 1
        return next_id
            
            
