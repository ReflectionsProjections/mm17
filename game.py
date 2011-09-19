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
		self.log_file = open(log_file, 'a')
		self.players = players
		self.actions = [] # list of dicts, index for turn [player] for player
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
		"""Starts the game turn loop."""
		self.active = True
		self.last_turn_time = time.time()
		self._log("Game started.")

	def _end(self):
		"""Stops the game main loop."""
		self._log("Game ended.")
		self.active = False

	def _resolve_turn(self):
		"""Executes a list of actions given by the players."""
		# Clear events from previous turn
		for ship in self.game_map.ships.itervalues():
			del ship.events[:]
		
		for action in self.actions.iteritems():
			for ship, vector in action.thrust.iteritems():
				ship.thrust(vector)
			for ship, angle in action.fire.iteritems():
				ship.fire(angle,self.game_map)
		self.actions = {}

		deadships = []
		for ship in self.game_map.objects.itervalues():
			for e in ship.events:
				pass
				# read damage records, compute new hp
			if ship.health < 0:
				deadships.append(ship)
				ship.health = 0
				del ship.events[:]
			else:
				pass
				# compute radar returns, extend events

		self.player_results = {}
		for p in self.players:
			self.player_results = \
			[{'id' : ship.id,
			  'health' : ship.health,
			  'position' : ship.position,
			  'velocity' : ship.velocity,
			  'events' : ship.events} \
			 for ship in self.game_map.objects.itervalues() \
			 if ship.owner is p]

		# clear out dead ships
		for ship in deadships:
			del self.game_map[ship.id]
			ship.owner.ship_count -= 1
		# clear out defeated players
		deadplayers = []
		for p in players:
			if p.ship_count == 0:
				deadplayer.append(p)
		#remove?

		for ship in self.game_map.itervalues():
			ship.step(1) # take timestep
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
					turns_submitted++
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
