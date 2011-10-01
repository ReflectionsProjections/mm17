#! /usr/bin/env python
import unittest
from urllib2 import urlopen
import json
from math import pi
players = {'one':'asdfg'}

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
	url = "http://localhost:7000/game/turn"
	data = {'auth':'asdfg',
			'actions':[]}

	for obj in json.loads(test_info_all())['objects']:
		id = obj['id']
		action = {'obj_type':'ship',
				'obj_id': id,
				'command': 'thrust',
				'args': { 'accel': (1, 1)}}
		data['actions'].append(action)
		action = {'obj_type':'ship',
				'obj_id': id,
				'command': 'fire',
				'args': { 'angle': pi}}
		data['actions'].append(action)
	return urlopen(url, json.dumps(data)).read()

if __name__ == '__main__':
	print test_join()
	print test_info()
	print "Testing /game/info/all GET"
	print test_info_all()
	print "Testing /game/turn POST"
	print test_actions()
