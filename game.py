#! /usr/bin/env python

from datetime import datetime
import time
from ship import Ship
from player import Player
import thread

class Game(object):
	"""The main Game class runs the game. This class accumulates
	and applies orders, provides turn results, and logs data.

	The Game directly stores the log file, the set of players,
	a set of pending orders for each player, the current turn,
	and whether the game is in progress.

	Ship information is stored in the game map.

	The game contains the logic for deciding when to take
	a turn, and for resolving a turn.
	"""

	def __init__(self, game_map, log_file):
		"""Initialize the game object

		@param game_map: Map object for the game
		@param log_file: Path to log file. Will be overwritten
		"""
		self.game_map = game_map
		self.players = {}
		self.log_file = open(log_file, 'w')
		# List of orders for each turn, dictionaries indexed by player
		self.actions = [{}]
		# Player results, indexed by players
		self.player_results = {}
		self.turn = 0
		self.active = False

	def _log(self, message):
		"""Log a single-line message.

		Formatted with a timestamp and a trailing newline."""
		text = "%s: %s\n" % (datetime.now(), message)
		self.log_file.write(text)

	def _begin(self):
		"""Create starting units and start the game turn loop."""

		for player in self.players.itervalues():
			new_ship = Ship(self, (0,0), player)
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
		"""Apply all the orders which have been recieved for this turn,
		update the game state to the start of the next turn,
		and calculate reponses for each player."""

		actions = self.actions[self.turn]
		results = {}

		for ship in self.game_map.objects.itervalues():
			ship.events = []

		# execute orders
		for player , actions in actions.iteritems():
			for action in actions:
				obj = self.game_map.objects[actions['obj_id']]
				method = getattr(obj, action['method'])
				method(**action['params'])

		#apply effects
		for ship in self.game_map.objects.itervalues():
			if ship.health <= 0:
				# kill dead ships
				ship.alive = False
				ship.health = 0
				ship.results[self.turn] = self.events[:]
				ship.events = [{'status':'destroyed'}]
			else:
				# compute radar returns for live ships
				nearships = self.game_map.radar(ship.position, ship.range)
				for other in nearships:
					scan = ship.scan(other)
					if scan:
						ship.events.append(scan)
				ship.results[self.turn] = self.events[:]

		# Create a massive list of results to return to the player
		self.player_results[self.turn] = {}
		for p in self.players.iterkeys():
			self.player_results[self.turn][p] = \
					[object._to_dict() \
					for object in self.game_map.objects.itervalues() \
					if object.owner == self.players[p]]

		# kill players with no live units
		for p in self.players.itervalues():
			for x in p.objects.itervalues():
				if x.alive:
					break
			else:
				p.alive = False

		# take timestep
		for object in self.game_map.objects.itervalues():
			object.step(1)
			object.results[self.turn + 1] = []

		# advnace turn and reset timer
		self.turn += 1
		self.actions.append({})
		self.last_turn_time = time.time()
		return

	def _main(self):
		"""Game main thread. Polls for turns being ready.

		Started by _begin(). Calls _end when one player remains.
		Resolves a turn when timeout passes or all players have
		submitted moves."""

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

	def last_turn_info(self):
		"""Current turn as {'turn' : turn}."""
		return {
			'turn': self.turn,
		}

	def game_info(self):
		"""Return basic game status.

		Fields are
		game_active - true if game is in progress
		turn - upcoming turn number
		active_players - list of player names"""
		active_players = []
		for player in self.players.itervalues():
			if player.alive:
				active_players.append(player.name)

		return {
			'game_active': self.active,
			'turn':self.turn,
			'active_players': active_players
		}

	def game_info_all(self, auth):
		"""Return game state including objects of player with given auth code.

		@param auth: authCode of the player making the requests."""
		alive_players = []
		for player in self.players.itervalues():
			if player.alive:
				alive_players.append(player.name)
		player = self.players[auth]
		return {
			'game_active': self.active,
			'turn':self.turn,
			'alive_players': alive_players,
			'objects': [object._to_dict() for object in\
					self.game_map.objects.itervalues()]
		}

	def add_player(self, name, authToken):
		""" Adds a player to the current game, begin game if now full.

		@param name: Name of player
		@param authToken: player token"""
		newPlayer = Player(name, authToken)
		if len(self.players.keys()) >= self.game_map.max_players:
			return {'join_success': False,
				'message': 'Game full'}
		if authToken in self.players.keys():
			return {'join_success': False,
				'message': 'Already joined'}

		self.players[authToken] = newPlayer
		self._log(name + " joined the game.")

		if len(self.players.keys()) == self.game_map.max_players:
			self._begin()

		return {'join_success': True,
			'message': 'Joined succesfully'}

import unittest
from game_map import Map

class TestGame(unittest.TestCase):
	def setUp(self):
		self.game_map = Map(2)
		self.game = Game(self.game_map,"test_log")

	def tearDown(self):
		self.game.active = False
		# thread should eventually kill itself, if it is running
		del self.game_map
		del self.game

	def testLastTurnInfo(self):
		self.assertEqual({'turn':0},self.game.last_turn_info())

	def testGameInfo(self):
		self.assertEqual(
			{'game_active':False,
			'turn':0,
			'active_players':[]},
			self.game.game_info())

	def testJoining(self):

		# game does not start until we have enough players
		self.assertFalse(self.game.active)

		# adding a player
		self.assertTrue(
			self.game.add_player('bob','123456')['join_success'])

		# game does not start until we have enough players
		self.assertFalse(self.game.active)

		# duplicate token
		self.assertFalse(
			self.game.add_player('ted','123456')['join_success'])

		# second player
		self.assertTrue(
			self.game.add_player('goodPasswordMan','123456*7*')['join_success'])

		# game should have started
		self.assertTrue(self.game.active)

		# no more room
		self.assertFalse(
			self.game.add_player('late','xyzw')['join_success'])

if __name__ == '__main__':
	unittest.main()
