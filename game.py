import datetime
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
		self.turn = 0
		self.actions = [] # list of dicts, index for turn [player] for player
		self.player_results = {}

	def _log(self, message):
		""" Adds a message to the end of the log file. """
		text = "%s: %s" % (datetime.now, message)
		self.log_file.write(text)

	def _begin(self):
		"""Starts the game turn loop."""
		self.active = True
		self.last_turn_time = time.time()
		self._log("Game started.")

	def _end(self):
		"""Stops the game turn loop."""
		self._log("Game ended.")
		self.active = False

	def _resolve_turn(self):
		"""Executes a list of actions given by a player.
		Should be called by server."""
		for ship in self.game_map.objects.itervalues():
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

	def validate(self, player, actions):
		"""Filter down to well-formed and legal actions.
		Return a pair of a JSON description of the paring results,
		and a parsed representation of the actions"""
		valid = 0
		duplicate = 0
		wrong_owner = 0
		invalid_ship = 0
		malformed = 0

		thrust = {}
		fire = {}
		for a in actions:
			if not(hasattr(a,'command')) or \
			 not(a.command in ['thrust','fire']) or \
			 not(hasattr(a,'ship')):
				malformed += 1
			else:
				try:
					sid = int(a.ship)
				except ValueError:
					malformed += 1
				else:
					if sid not in self.game_map:
						invalid_ship += 1
					elif not(self.game_map[sid].owner is player):
						wrong_owner += 1
					else:
						if a.command == 'thrust':
							if sid in thrust:
								duplicate += 1
							else:
								if not(hasattr(a,'thrust')) or \
								 not(type(a.thrust) is list) or \
								 len(a.thrust) != 2:
									malformed += 1
								else:
									thrust[sid] = a.thrust
									valid += 1
						elif a.command == 'fire':
							if sid in fire:
								duplicate += 1
							else:
								if not(hasattr(a,'angle')) or \
								 not (type(a.angle) in [float,int,long]):
									malformed += 1
								else:
									fire[sid] = a.angle
									valid += 1
		self.actions[player] = {'thrust':thrust, 'fire':fire}
		if len(self.actions) == len(self.players):
			self._resolve_turn()
		return {'valid':valid,
				'duplicate':duplicate,
				'wrong_owner':wrong_owner,
				'invalid_ship':invalid_ship,
				'malformed':malformed}

	def info(self):
		information = {
			'turn': self.turn,
		}
