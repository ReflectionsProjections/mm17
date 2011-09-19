#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json, os
from urlparse import urlparse
from urlparse import parse_qs

from time import gmtime, strftime
from game import Game
from map import Map

class MMHandler(BaseHTTPRequestHandler):
	# This NEEDS to be inited inside of an __init__ method - but it doesn't seem to work. This is a hack for now.
	game_time = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
	game_name = 'logs/game-%s' % game_time
	game_map = Map(100, 100, 4)
	game = Game(game_map, game_name, {})
	def send_error(self, code, text):
		# send_error doesn't do JSON responses; we want json, so here's our own error thing
		self.send_response(code)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write(json.dumps({'error': text}))
	def respond(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_GET(self):
		parsedURL = urlparse(self.path)
		path = parsedURL.path[1:]
		params = parse_qs(parsedURL.query)

		if len(path) < 1:
			self.send_error(400, "Requests to the root are invalid. Did you mean /turn_info?")
			return
		if path  == 'turn_info':
			self.respond()
			output = json.dumps(self.game.lastTurnInfo())
			self.wfile.write(output)
			return
		elif path == 'game_info':
			gameStatus = self.game._gameInfo()
			self.respond()
			self.wfile.write(json.dumps(gameStatus))
			return
		elif path == 'join':
			if 'auth' not in params or 'name' not in params:
				self.send_error(400, "Auth code or name was not provided")
				return

			authCode = params['auth'][0]
			name = params['name'][0]

			successObj = self.game._addPlayer(name, authCode)
			self.respond()
			self.wfile.write(json.dumps(successObj))
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

		if input['auth_code'] == Game.current_player.auth_code:
			response = Game.handle_turn(input)
			self.send_error(response['code'])
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			writeout = json.dumps(response['output'])
			self.wfile.write(writeout)
			return
		else:
			self.send_error(403, "Wrong auth code! (Maybe it isn't your turn?")
			return

if __name__ == '__main__':
	port = 7000
	print "Starting on port " + str(port) + "..."
	server = HTTPServer(('', port), MMHandler)
	server.serve_forever()
