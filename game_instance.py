from time import gmtime, strftime
import os

from game import Game
from game_map import Map
try:
	os.mkdir('logs')
except OSError:
	pass

game_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
game_name = 'logs/game-%s' % game_time
game_map = Map(1)
game = Game(game_map, game_name)
