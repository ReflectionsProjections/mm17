#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 noexpandtab
"""
             __ __            _    __ __            _        _  ___
            |  \  \ ___  ___ | |_ |  \  \ ___ ._ _ <_> ___  / ||_  |
            |     |/ ._>/ | '| . ||     |<_> || ' || |<_> | | | / /
            |_|_|_|\___.\_|_.|_|_||_|_|_|<___||_|_||_|<___| |_|/_/
 _______ _    _ _____  _    _  _____ _______  __          __     _____   _____
|__   __| |  | |  __ \| |  | |/ ____|__   __| \ \        / /\   |  __ \ / ____|
   | |  | |__| | |__) | |  | | (___    | |     \ \  /\  / /  \  | |__) | (___
   | |  |  __  |  _  /| |  | |\___ \   | |      \ \/  \/ / /\ \ |  _  / \___ .
   | |  | |  | | | \ \| |__| |____) |  | |       \  /\  / ____ \| | \ \ ____) |
   |_|  |_|  |_|_|  \_\_____/|_____/   |_|        \/  \/_/    \_\_|  \_\_____/

                        Sample Client - Python 2.x

Copyright (c) 2011 Association for Computing Machinery.  All rights reserved.

Developed by: 2011 MechMania Programming Team, ACM@UIUC
              University of Illinois at Urbana-Champaiagn
              http://acm.uiuc.edu/conference/2011/mechmania.php

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal with the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
  1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimers.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimers in the
     documentation and/or other materials provided with the distribution.
  3. Neither the names of the MechMania Development Team, nor that of the
     University of Illinois at Urbana-Champaign, nor the names of its
     contributors may be used to endorse or promote products derived from
     this Software without specific prior written permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
WITH THE SOFTWARE.

"""


import json, time, sys
from urllib2 import urlopen
from urllib  import urlencode

class GameClient(object):
	"""
	Client object; an instance of this is created to play the game
	"""
	def __init__(self, url, name, authcode):
		"""
		Create a new client instance

		@param url: The base URL of the game server
		@param name: A name for this client
		@param authcode: The unique identifier of this client
		"""
		self.base = url          #: Base URL for the server
		self.name = name         #: Name of the client
		self.authcode = authcode #: Authentication code for the client
		self.running = False     #: Whether the client should continue to run
		self.current_turn = -1   #: The current turn, or -1 for "game hasn't started"
		self.objects = {}        #: Objects that the client knows about
	def _loop(self):
		"""
		Game Loop

		This is where all the important stuff happens.
		"""
		self._waitForNextTurn()
		print "Turn number %d..." % self.current_turn,
		game_state = self._do("game/info/all",{})
		actions = []
		for thing in game_state['objects']:
			if thing['type'] == "ship":
				actions.append({
					"obj_type": "ship",
					"obj_id": thing['id'],
					"command": "thrust",
					"args": { 
						"accel": (1,1)
						}
					})
		result = self._post("game/turn",{'actions': actions})
		failed = 0
		for r in result:
			if not r['success']:
				failed += 1
				return
		if failed == 0:
			print "Done."
		else:
			print "Done, but %d actions failed." % failed
	def _waitForNextTurn(self):
		"""
		Poll the server for the current turn until we have switched to the next turn.
		"""
		_break = False
		while not _break:
			time.sleep(0.2)
			status = self._do("game/info",{})
			if not status["game_active"]:
				if status['turn'] < 0:
					continue
				print "Game has ended. Stopping."
				sys.exit(0)
			if status['turn'] == self.current_turn + 1:
				_break = True
			else:
				print "Turn is %d..." % status['turn']
		self.current_turn += 1
	def _do(self, path, args):
		"""
		Perform a GET request to the requested path, with the requested arguments.

		@param path: Object identifier to request from the server
		@param args: A dictionary of arguments to pass as ?params=
		@return: Dictionary of the results from the server for the request
		"""
		if len(args) < 1: args = {}
		args['auth'] = self.authcode
		_url = self.base + "/" + path
		return json.loads(urlopen(_url + "?" + urlencode(args)).read())
	def _post(self, path, args):
		"""
		Perform a POST to the requested path, with the requested data.

		@param path: Object identifier to POST to on the server
		@param args: A dictionary of JSON data (in dictionary/list format) to POST
		@return: Dictionary of the results from the server for the POST
		"""
		if len(args) < 1: args = {}
		args['auth'] = self.authcode
		_url = self.base + "/" + path
		return json.loads(urlopen(_url, json.dumps(args)).read())
	def start(self):
		"""
		Start the client.
		"""
		print self._do("game/join",{"name":self.name})
		self.running = True
		while self.running:
			self._loop()


if __name__ == "__main__":
	code = raw_input("Auth code? ") # Wait for an auth code
	c = GameClient("http://localhost:7000", "NAME HERE", code) # Initialize the client
	c.start() # Start playing
