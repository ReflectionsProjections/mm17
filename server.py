#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json, os
from urlparse import urlparse
from urlparse import parse_qs

from time import gmtime, strftime
from game import Game
from gamemap import Map
from validate import handle_input

class MMHandler(BaseHTTPRequestHandler):
	game_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
	game_name = 'logs/game-%s' % game_time
	game_map = Map(1)
	game = Game(game_map, game_name)

	# URI Handling Functions

	def game_info(self, params):
		""" Handles a request for the game state, which includes
		active players and whether or not the game has started """
		gameStatus = self.game.game_info()
		self.respond()
		self.wfile.write(json.dumps(gameStatus))
		return

	def game_info_all(self, params):
		""" Handles a request for the game state, which includes all 
		info available to the player """
		gameStatus = self.game.game_info_all(params['auth'][0])
		self.respond()
		self.wfile.write(json.dumps(gameStatus))
		return

	def game_turn_get(self, params):
		""" Handles a GET request for the game state at the most
		recent completed turn """
		self.respond()
		output = json.dumps(self.game.last_turn_info())
		self.wfile.write(output)
		return

	def game_turn_post(self, input):
		""" Handles a POST request for the next turn"""
		self.respond()
		output = json.dumps(handle_input(input, self.game))
		self.wfile.write(output)
		return

	def game_join(self, params):
		""" Handles a request to join the game """
		if 'auth' not in params or 'name' not in params:
			self.send_error(400, "Auth code or name not provided")
			return

		authCode = params['auth'][0]
		name = params['name'][0]

		successObj = self.game.add_player(name, authCode)
		self.respond()
		self.wfile.write(json.dumps(successObj))
		return

	# These map URIs to handlers depending on request method
	GET_PATHS = {
		'game': {
			'info': {
				'': game_info,
				'all':game_info_all
				},
			'turn': game_turn_get,
			'join': game_join,
		},
	}

	POST_PATHS = {
		'game': {
			'turn': game_turn_post,
		},
	}


	# Other helper functions

	def explode_path(self, parsedURL):
		exploded_path = parsedURL.path[1:].split('/')
		search_paths = []

		if exploded_path[0] == '':
			self.send_error(400, "Requests to the root are invalid. Did you mean /game/turn?")
			return

		for path in exploded_path:
			if path is not '':
				search_paths.append(path)
		search_paths.append('')
		return search_paths


	def walk_path(self, search_dict, search_path):
		""" Walk the PATHS object to find the correct handler based upon
		the URI queried """
		first_item = search_path.pop(0)
		if first_item in search_dict:
			if isinstance(search_dict[first_item], dict):
				return self.walk_path(search_dict[first_item], \
						      search_path)
			else:
				return search_dict[first_item]
		else:
			return None

	def send_error(self, code, text):
		# send_error doesn't do JSON responses; we
		# want json, so here's our own error thing
		self.send_response(code)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write(json.dumps({'error': text}))

	def respond(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	# HTTP Request Handlers

	def do_GET(self):
		parsedURL = urlparse(self.path)
		params = parse_qs(parsedURL.query)

		search_paths = self.explode_path(parsedURL)
		handler = self.walk_path(self.GET_PATHS, search_paths)
		if handler is not None:
			handler(self, params)
			return
		else:
			self.send_error(404, "Unknown resource identifier: %s" % self.path)
			return

	def do_POST(self):
		length = int(self.headers.getheader('content-length'))
		rfile = self.rfile.read(length)
		try:
			input = json.loads(rfile)
		except ValueError:
			self.send_error(400, "Bad JSON.")
			return
		parsedURL = urlparse(self.path)
		search_paths = self.explode_path(parsedURL)
		handler = self.walk_path(self.POST_PATHS, search_paths)
		if handler is not None:
			handler(self, input)
			return
		else:
			self.send_error(404, "Unknown resource identifier: %s"\
						% self.path)
			return



if __name__ == '__main__':
	port = 7000
	print "Starting on port " + str(port) + "..."
	server = HTTPServer(('', port), MMHandler)
	server.serve_forever()
