from datetime import datetime
import time
from player import Player

class Game(object):
	"""The main Game class runs the game and contains the main loop
	that updates statuses and logs data."""

	def __init__(self, game_map, log_file, players):
		"""Initialize the game object

		Arguments:
		game_map - Map object for the game
		log_file - Path to log game data to
		players - A list of the game's players
		"""
		self.game_map = game_map
		self.log_file = open(log_file, 'w')
		self.players = players
		self.actions = [] # list of dicts, index for turn, [player] for player
		self.player_results = {}
		self.turn = 0
		self.active = False
	
	def _gameInfo(self):
		active_players = []
		for key, player in self.players.items():
			if player.alive:
				active_players.append(player.name)

		status = {
			'game_active': self.active,
			'active_players': active_players
		}
		return status

	def _addPlayer(self, name, authToken):
		""" Adds a player to the current game """
		newPlayer = Player(name, authToken)
		if len(self.players.keys()) < self.game_map.maxPlayers:
			if authToken not in self.players:
				self.players[authToken] = newPlayer
			else:
				return {'join_success': False, 'message': 'Already joined'}

			if len(self.players.keys()) == self.game_map.maxPlayers:
				self._begin()
			return {'join_success': True, 'message': 'Joined succesfully'}
		else:
			return {'join_success': False, 'message': 'Game full'}

	def _log(self, message):
		""" Adds a message to the end of the log file. """
		text = "%s: %s" % (datetime.time(), message)
		self.log_file.write(text)

	def _begin(self):
		"""Sets up beginning state and starts the game turn loop."""
		for player in self.players:
			new_ship = Ship(self, player, (0,0))
			self.game_map.add_object(new_ship)
			player.add_object(new_ship)
		self.active = True
		self.last_turn_time = time.time()
		self._log("Game started.")

	def _end(self):
		"""Stops the game main loop."""
		self._log("Game ended.")
		self.active = False

	def _resolve_turn(self):
		"""Executes a list of actions given by the players."""
		
		actions = self.actions[self.turn]
		for player in self.actions.iteritems():
			for action in player:
				obj = self.game_map.objects[action['obj_id']]
				method = getattr(obj, action['method'])
				obj.results[self.turn]\
				    .append(method(**action['params']))

		for object in self.game_map.objects.itervalues():
			for event in object.events:
				pass
				# read damage records, compute new hp
			if object.health < 0:
				object.alive == False
				object.health = 0
				object.results[self.turn]\
				    .append({'status':'destroyed'})
			else:
				pass
				# compute radar returns, extend events

		# Create a maasive list of results to return to the player
		for p in self.players:
			self.player_results[self.turn][p] = \
			[object.get_state()
			 for object in self.game_map.objects.itervalues() \
			 if object.owner is p]


		# clear out defeated players
		for p in players:
			alive = [x for x in p.objects if x.alive]
			if len(alive) == 0:
				p.alive = False

		# take timestep
		for object in self.game_map.objects.itervalues():
			object.step(1)

		# advnace turn and reset timer
		self.turn += 1
		self.last_turn_time = time.time()

	def _main(self):
		"""Loops and waits for all turns to be submitted.  Called by
		_begin() and ends by _end().  Also checks for exit condition.
		"""
		while self.active == True:
			alive_players = [x for x in self.players if x.alive == True]
			if alive_players <= 1:
				self._end()
			turns_submitted = 0
			for player, action in self.actions[self.turn]:
				if action:
					turns_submitted+=1
			if turns_submitted == len(alive_players):
				self._resolve_turn()
			elif time.time() - self.last_turn_time > 2:
				self._resolve_turn()
			else: 
				continue

	def lastTurnInfo(self):
		information = {
			'turn': self.turn,
		}



class GameObject(object):
	"""Base class for all game objects on the map since they need 
	certain common info"""
	def __init__(self, game, position, owner):
		self.game = game
		self.position = position
		self.velocity = (0,0)
		self.owner = owner
		self.alive = True

		# holds all events to be processed on turn handle
		# list of lists accessed like events[turn]
		self.events = []

		# holds results from turns to be returned to user
		# list of lists accessed like results[turn]
		self.results = []

	def step(self, dt):
		vx, vy = self.velocity
		x, y = self.position
		self.position = (x + dt*vx, y + dt*vy)

	def get_state(self):
		state = {'obj_id': id(self),
			 'owner': self.owner,
			 'position':self.position,
			 'alive': self.alive,
			 'results':self.results[game.turn]
			 }
		return state
