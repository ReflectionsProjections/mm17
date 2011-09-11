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
		input = json.loads(self.rfile.read())
		response = Game.handle_turn(input)
		self.send_response(response.code)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		writeout = json.dumps(response.output)
		self.wfile.write(writeout)
		return 

if __name__ == '__main__':
	port = 7000
	print "Starting on port " + str(port) + "..."
	server = HTTPServer(('', port), MMHandler)
	server.serve_forever()
