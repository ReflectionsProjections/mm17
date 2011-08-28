#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class MMHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write("{ herp: \"derp\" }")
		return
	def do_POST(self):
		return

if __name__ == '__main__':
	print "Starting..."
	server = HTTPServer(('',7000), MMHandler)
	server.serve_forever()
