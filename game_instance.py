from time import gmtime, strftime
import os

from game import Game
from game_map import Map
try:
	os.mkdir('logs')
except OSError:
	pass
viz_auth = '123456'
game_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
log_file = 'logs/game-%s' % game_time
game_map = Map(1)
game = Game(game_map, log_file, viz_auth)
