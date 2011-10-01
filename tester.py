#! /usr/bin/env python
import unittest
from urllib2 import urlopen
import json
from math import pi
players = {'one':'asdfg',
		   'two':'adad'}

def test_join():
	output = ""
	for name, auth in players.items():
		url = "http://localhost:7000/game/join?name="+name+"&auth="+auth
		output += urlopen(url).read() + '\n'
	return output

def test_info():
		url = "http://localhost:7000/game/info"
		return urlopen(url).read()

def test_info_all():
		url = "http://localhost:7000/game/info/all?auth=asdfg"
		return urlopen(url).read()

def test_actions():
	output = ""
	derp = json.loads(test_info_all())
	for key, value in players.items():
		url = "http://localhost:7000/game/turn/"+str(json.loads(test_info())['turn'])
		data = {'auth' : value,
				'actions':[]}
		for obj in derp['objects']:
			if obj['type'] == 'ship' and obj['owner'] == value:
				id = obj['id']
				action = {'obj_type':'ship',
						  'obj_id': id,
						  'command': 'thrust',
						  'args': { 'direction': (1, 1),
								'speed':10}}
				data['actions'].append(action)
				action = {'obj_type':'ship',
						  'obj_id': id,
						  'command': 'fire',
						  'args': { 'direction': (1,2)}}
				data['actions'].append(action)
				output+= urlopen(url, json.dumps(data)).read() + '\n'
	return output
if __name__ == '__main__':
	print test_join()
	print test_info()
	print "Testing /game/info/all GET"
	print test_info_all()
	print "Testing /game/turn POST"
	print test_actions()
