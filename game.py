#! /usr/bin/env python

import time
import thread
import threading
import unittest
import os

from datetime import datetime
import Constants

class Game(object):
	"""
	The main Game class runs the game. This class accumulates
	and applies orders, provides turn results, and logs data.

	The Game directly stores the log file, the set of players,
	a set of pending orders for each player, the current turn,
	and whether the game is in progress.

	Ship information is stored in the game map.

	The game contains the logic for deciding when to take
	a turn, and for resolving a turn.
	"""

	def __init__(self, game_map, log_file):
		"""
		Initialize the game object.

		@type  game_map: game_map object
		@param game_map: Map object for the game

		@type  log_file: string
		@param log_file: Path to log file. Existing file at this path
				will be overwritten.
		"""
		self.game_map = game_map
		self.allowed_auths = []
		self.viz_auth = ''
		self.players = {}
		self.log_file = open(log_file, 'w')
		# List of orders for each turn, dictionaries indexed by player
		self.action_list_lock = threading.Lock()
		with self.action_list_lock:
			self.actions = [{}]
			self.completed_turns = [{}]
		# Player results, indexed by players
		self.player_result_lock = threading.Lock()
		self.lasers_shot_lock = threading.Lock()
		with self.player_result_lock:
			self.player_results = {}
		self.turn = 0
		self.active = False
		self.lasers_shot = [[]]

	def _log(self, message):
		"""
		Log a single-line message. Formatted with a timestamp and a
		trailing newline.

		@type  message: string
		@param message: Message to write out to the log file
		"""
		text = "%s: %s\n" % (datetime.now(), message)

		self.log_file.write(text)

	def _begin(self):
		from game_map import map_maker
		"""
		Create starting units and start the game turn loop.
		"""
		map_maker(self.players)
		self.active = True
		self.last_turn_time = time.time()
		self._log("Game started.")
		# is this a good idea?
		thread.start_new_thread(self._main, ())

	def _end(self):
		"""
		Stop the game main loop.
		"""
		self._log("Game ended.")
		self.active = False

	def _resolve_turn(self):
		from ship import Ship
		"""
		Apply all the orders which have been recieved for this turn,
		update the game state to the start of the next turn, and
		calculate reponses for each player.
		"""
		with self.action_list_lock:
			actions = self.actions[self.turn]
		results = {}
		refineries = [x.refinery for x in \
						  self.game_map.asteroids.itervalues() if x.refinery]
		bases = [x.base for x in self.game_map.planets.itervalues() if x.base]
		for obj in self.game_map.objects.itervalues():
			obj.events = []
		for obj in bases + refineries:
			obj.events = []
		# execute orders
		with self.action_list_lock:
			for player , actions in actions.iteritems():
				for action in actions:
					method = getattr(action['object'], action['method'])
					method(**action['params'])
		#apply effects
		ownables = refineries + bases + self.game_map.ships.values()
		for obj in ownables:
			for event in obj.events:
				if event['type'] == 'damage':
					obj.health -= event['amount']
			if obj.health <= 0:
				# kill dead objects
				obj._delete()
			else:
				# compute radar returns for live ships
				nearships = self.game_map.radar(obj)
				for other in nearships:
					if other != self:
						obj.events.append({'type':'radar',
											'id': id(other),
											'position':other.position})
				obj.results[self.turn] = obj.events[:]

		# Create a massive list of results to return to the player
		with self.player_result_lock:
			self.player_results[self.turn] = {}
			for key, value in self.players.iteritems():
				self.player_results[self.turn][key] = \
					[object.to_dict() \
						 for object in value.objects.itervalues()]
			# kill players with no live units
				live_bases = [x for x in value.bases.values() if x.alive]
				live_ships = [x for x in value.ships.values() if x.alive] 
				if len(live_ships) == 0 and len(live_bases) == 0:
					value.alive = False
				# update resources and scores
				value.update_resources()
				value.update_score()
					
		# take timestep
		for object in self.game_map.objects.itervalues():
			object.step(1)
			object.results[self.turn + 1] = []
			if isinstance(object, Ship):
				for method in object.methods_used.iterkeys():
					object.methods_used[method] = False

		# subtract from busy and build counters
			if hasattr(object, 'base') and object.base != None:
				if object.base.built > 0:
					object.base.built -= 1
				if object.base.busy > 0:
					object.base.busy -= 1

			if hasattr(object, 'refinery') and object.refinery != None:
				if object.refinery.built > 0:
					object.refinery.built -= 1
				if object.refinery.busy > 0:
					object.refinery.busy -= 1

		# advnace turn and reset timer
		with self.action_list_lock:
			self.actions.append({})
			self.completed_turns.append({})
			self.turn += 1
		with self.lasers_shot_lock:
			self.lasers_shot.append([])
		self.last_turn_time = time.time()

	def _main(self):
		"""
		Game main thread. Polls for turns being ready.

		Started by _begin(). Calls _end when one player remains.
		Resolves a turn when timeout passes or all players have
		submitted moves.
		"""

		while self.active == True:
			alive_players = [x for x in self.players.itervalues() if x.alive]
			if len(alive_players) <= 1:
				self._end()
			with self.action_list_lock:
				turns_submitted = len(self.completed_turns[self.turn])
			if turns_submitted == len(alive_players):
					self._resolve_turn()
			#elif time.time() - self.last_turn_time > 2:
			#	self.busy = True
			#	self._resolve_turn()
			else:
				continue

	def get_player_by_auth(self, auth):
		"""
		Get player object via their auth code.
		@param auth: auth string
		@rtype: Player object
		@return: Player object or None
		"""
		players = [x for x in self.players.values() if x.auth == auth]
		if len(players) > 0:
			return players[0]
		else:
			return None

	# API Calls

	def turn_number(self):
		"""
		Get turn number.

		@rtype: dictionary
		@return: Current turn as {'turn' : turn}.
		"""
		return {
			'turn': self.turn
		}

	def game_status(self):
		"""
		Return basic game status.

		@rtype: dictionary
		@return: Dictionary with fields game_active, turn, and
				active_players, which contain the boolean status of the
				game, the upcoming turn, and the list of active players.
		"""
		active_players = []
		for player in self.players.itervalues():
			if player.alive:
				active_players.append(player.name)

		return {
			'game_active': self.active,
			'turn':self.turn,
			'active_players': active_players
		}

	def game_turn_get(self, auth, turn):
		"""
		Returns the player_results from the requested turn.
		"""
		if turn > 0 and turn < self.turn:
			player = self.get_player_by_auth(auth)
			if player == None:
				return {'success':False, 'message':'bad auth'}
			with self.player_result_lock:
				return player_results[turn - 1][id(player)]
		else:
			return {'success':False, 'message':'invalid turn number'}

	def game_avail_info(self, auth):
		"""
		Return game state including objects of player with given auth code.

		@type  auth: string
		@param auth: authCode of the player making the requests.
		"""
		alive_players = []
		for player in self.players.itervalues():
			if player.alive:
				alive_players.append(player.name)
		player = self.get_player_by_auth(auth)
		if player == None:
			return {'success':False, 'message':'bad auth'}
		return {
			'game_active': self.active,
			'turn':self.turn,
			'you': id(player),
			'alive_players': alive_players,
			'objects': [object.to_dict() for object in\
					player.objects.itervalues()],
		}

	def add_player(self, name, auth):
		from player import Player
		"""
		Adds a player to the current game, begin game if now full.

		@type  name: string
		@param name: Name of player

		@type  authToken: string
		@param authToken: player token
		"""
		if self.get_player_by_auth(auth):
			return {'join_success': False,
				'message': 'Already joined'}
		if auth not in self.allowed_auths:
			return {'join_success': False,
				'message': 'Not a valid auth code.'}
		if len(self.players.keys()) >= self.game_map.max_players:
			return {'join_success': False,
				'message': 'Game full'}

		new_player = Player(name, auth)
		self.players[id(new_player)] = new_player
		self._log(name + " joined the game.")

		if len(self.players.keys()) == self.game_map.max_players:
			self._begin()
		self.allowed_auths.remove(auth)
		return {'join_success': True,
			'message': 'Joined succesfully'}

	def game_visualizer(self, auth):
		"""
		Return all objects to the visualizer.

		@return: list of all objects
		"""
		if auth != self.viz_auth:
			return {'message':'not a valid auth code'}
		else:
			return {'turn':self.turn, 
					'objects':[o.to_dict() for o in\
								   self.game_map.objects.values()], 
					'players':[p.to_dict() for p in self.players.values()], 
					'lasers':self.lasers_shot[self.turn - 1]}
			
class TestGame(unittest.TestCase):
	def setUp(self):
		from game_map import Map
		self.game_map = Map(2)
		self.game = Game(self.game_map,"test_log")

	def tearDown(self):
		self.game.active = False
		# thread should eventually kill itself, if it is running
		del self.game_map
		del self.game

	def test_turn_number(self):
		self.assertEqual({'turn':0},self.game.turn_number())

	def testGameInfo(self):
		self.assertEqual(
			{'game_active':False,
			'turn':0,
			'active_players':[]},
			self.game.game_status())

 
if __name__ == '__main__':
	unittest.main()
