import datetime
from player import Player

class Game(object):
	"""The main Game class runs the game and contains the main loop
	that updates statuses and logs data."""

	def __init__(self, map, log_file, players):
		self.map = map # map object
		self.log_file = log_file # should be a path
		self.players = players # list of players
		self.moves = {}
		self.player_results = {}
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
		self._main()

	def _end(self):
		self._log("Game ended.")
		self.active = False

	def _resolve_turn(self):
		"""Executes a list of actions given by a player.
		Should be called by server."""
		for ship in self.map.objects.itervalues():
			del ship.events[:]
		for action in self.actions.iteritems():
			for ship, vector in action.thrust.iteritems():
				ship.thrust(vector)
			for ship, angle in action.fire.iteritems():
				ship.fire(angle,self.map)
		self.actions = {}

		deadships = []
		for ship in self.map.objects.itervalues():
			for e in ship.events:
				# read damage records, compute new hp
			if ship.health < 0:
				deadships.append(ship)
				ship.health = 0
				del ship.events[:]
			else:
				# compute radar returns, extend events

		self.player_results = {}
		for p in self.players:
			self.player_results =
			[{'id' : ship.id,
			  'health' : ship.health,
			  'position' : ship.position,
			  'velocity' : ship.velocity,
			  'events' : ship.events}
			 for ship in self.map.objects.itervalues()
			 if ship.owner is p]

		# clear out dead ships
		for ship in deadships:
			del map[ship.id]
			ship.owner.ship_count -= 1
		# clear out defeated players
		deadplayers = []
		for p in players:
			if p.ship_count == 0:
				deadplayer.append(p)
		#remove?

		for ship in self.map.itervalues():
			ship.step(1) # take timestep
		self.turn += 1

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
			if not(hasattr(a,'command')) or
			   not(a.command in ['thrust','fire']) or
			   not(hasattr(a,'ship')):
			   malformed += 1
			elif 
				try sid = int(a.ship):
				except ValueError:
					malformed += 1
				else:
					if sid not in self.map:
						invalid_ship += 1
					elif not(self.map[sid].owner is player):
						wrong_owner += 1
					else:
						if a.command == 'thrust':
							if sid in thrust:
								duplicate += 1
							else:
								if not(hasattr(a,'thrust')) or
								   not(type(a.thrust) is list) of
								   len(a.thrust) != 2:
								   malformed += 1
								else:
									thrust[sid] = a.thrust
									valid += 1
						elif a.command == 'fire':
							if sid in fire:
								duplicate += 1
							else:
								if not(hasattr(a,'angle')) or
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
