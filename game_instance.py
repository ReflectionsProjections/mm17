from time import gmtime, strftime
from game import Game
from game_map import Map
game_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
game_name = 'logs/game-%s' % game_time
game_map = Map(1)
game = Game(game_map, game_name)
