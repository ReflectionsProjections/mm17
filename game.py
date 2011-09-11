import datetime
import Player

class Game(object):
    """The main Game class runs the game and contains the main loop
    that updates statuses and logs data."""

    def __init__(self, map, log_file, players):
        self.map = map # map object
        self.log_file = log_file # should be a path
        self.players = players.shuffle() # list of players
        self.turn = 0

    def _log(self, message):
        """ Adds a message to the end of the log file. """
        with open(self.log_file, 'a') as log:
            text = "%s: %s" % (datetime.now, message)
            log.write(text)

    def _begin(self):
        self.active = True
        self.start_time = datetime.now
        self._log("Game started.")
        self.current_player = players[0]
        self._main()

    def _end(self):
        self._log("Game ended.")
        self.active = False

    def _add_player(self, name, color):
        new_player = Player(name, id = len(self,players), color)
        self.players.append(new_player)

    def _check_players(self):
        actives = [player for player in self.players if player.active == True]
        if len(actives) > 1: return True
        else: return False

    def _main(self):
        while self.active == True:
            if _check_players == False: self._end
            self._handle_turn()

    def next_id(self):
        self.next_id += 1
        return next_id
            
    def _handle_turn(self):
        self.turn += 1
        for action in self.current_player.actions:
            object = Map.objects[action['object'])]
            if hasattr(object, action['method']):
              method = getattr(object, action['method'])
              method(**action['kwargs']
            else:
                _log('%s attempted to use method %s with object %s, which failed' % (player.name, action['method'], action['object']))
        self.current_player = self.players[self.turn % len(self.players)]
        
