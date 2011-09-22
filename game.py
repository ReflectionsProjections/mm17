from datetime import datetime
import time
from ship import Ship
from player import Player
import thread

class Game(object):
	"""The main Game class runs the game and contains the main loop
	that updates statuses and logs data."""

	def __init__(self, game_map, log_file):
		"""Initialize the game object

		Arguments:
		game_map - Map object for the game
		log_file - Path to log game data to
		players - A list of the game's players
		"""
		self.game_map = game_map
		self.players = {}
		self.log_file = open(log_file, 'w')
		# list of dicts, index for turn, [player] for player
		self.actions = [{}] 
		self.player_results = {}
		self.turn = 0
		self.active = False
	
	def _log(self, message):
		""" Adds a message to the end of the log file. """
		text = "%s: %s\n" % (datetime.now(), message)
		self.log_file.write(text)

	def _begin(self):
		"""Sets up beginning state and starts the game turn loop."""
		for player in self.players.itervalues():
			new_ship = Ship(self, player, (0,0))
			self.game_map.add_object(new_ship)
			player.add_object(new_ship)
		self.active = True
		self.last_turn_time = time.time()
		self._log("Game started.")
		# is this a good idea?
		thread.start_new_thread(self._main, ())
		return

	def _end(self):
		"""Stops the game main loop."""
		self._log("Game ended.")
		self.active = False

	def _resolve_turn(self):
		"""Executes a list of actions given by the players."""
		
		actions = self.actions[self.turn]

		for player in actions.itervalues():
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
		self.player_results[self.turn] = {}
		for p in self.players.iterkeys():
			self.player_results[self.turn][p] = \
			[object.get_state() \
			 for object in self.game_map.objects.itervalues() \
			 if object.owner == self.players[p]]


		# clear out defeated players
		for p in self.players.itervalues():
			alive = [x for x in p.objects.itervalues() if x.alive]
			if len(alive) == 0:
				p.alive = False

		# take timestep
		for object in self.game_map.objects.itervalues():
			object.step(1)
			object.results[self.turn + 1] = []
			del object.events[:]

		# advnace turn and reset timer
		self.turn += 1
		self.actions.append({})
		self.last_turn_time = time.time()
		return

	def _main(self):
		"""Loops and waits for all turns to be submitted.  Called by
		_begin() and ends by _end().  Also checks for exit condition.
		"""
		while self.active == True:
			alive_players = [x for x in self.players.itervalues() \
						 if x.alive == True]
			if alive_players <= 1:
				self._end()
			turns_submitted = 0
			for actions in self.actions[self.turn].itervalues():
				if actions:
					turns_submitted+=1
			if turns_submitted == len(alive_players):
				self._resolve_turn()
			elif time.time() - self.last_turn_time > 2:
				self._resolve_turn()
			else: 
				continue

	# API Calls

	def last_turnI_info(self):
		information = {
			'turn': self.turn,
		}

	def game_info(self):
		active_players = []
		for player in self.players.itervalues():
			if player.alive:
				active_players.append(player.name)

		status = {
			'game_active': self.active,
			'turn':self.turn,
			'active_players': active_players
		}
		return status

	def game_info_all(self, auth):
		alive_players = []
		for player in self.players.itervalues():
			if player.alive:
				alive_players.append(player.name)
		player = self.players[auth]
		status = {
			'game_active': self.active,
			'turn':self.turn,
			'alive_players': alive_players,
			'objects': [object._to_dict() for object in\
					    self.game_map.objects.itervalues()]
		}
		return status

	def add_player(self, name, authToken):
		""" Adds a player to the current game """
		newPlayer = Player(name, authToken)
		if len(self.players.keys()) < self.game_map.maxPlayers:
			if authToken in self.players.keys():
				return {'join_success': False, 
					'message': 'Already joined'}
			else:
				self.players[authToken] = newPlayer
				self._log(name + " joined the game.")
				if len(self.players.keys()) == \
					    self.game_map.maxPlayers:
					self._begin()
				return {'join_success': True, 
					'message': 'Joined succesfully'}
		else:
			return {'join_success': False, 
				'message': 'Game full'}
