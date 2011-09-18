#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json, os
from game import Game

class MMHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/turn_info':
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			output = json.dumps(Game.info())
			self.wfile.write(output)

		elif self.path == '/tester':
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			with open(os.getcwd() + '/tester.html', 'r') as tester:
				self.wfile.write(tester.read())
		else:
			self.send_response(404)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			writeout = "Wrong path."
			self.wfile.write(writeout)
		return

	def do_POST(self):
		length = int(self.headers.getheader('content-length'))
		rfile = self.rfile.read(length)
		try:
			input = json.loads(rfile)
		except ValueError:
			self.send_error(400, "Bad JSON.")

		if input['auth_code'] == Game.current_player.auth_code:
			response = Game.handle_turn(input)
			self.send_error(response['code'])
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			writeout = json.dumps(response['output'])
			self.wfile.write(writeout)
		else:
			self.send_error(403, "Wrong auth code! (Maybe it isn't your turn?")
		return

if __name__ == '__main__':
	port = 7000
	print "Starting on port " + str(port) + "..."
	server = HTTPServer(('', port), MMHandler)
	server.serve_forever()
