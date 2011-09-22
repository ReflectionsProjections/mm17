#! /usr/bin/env python
from urllib2 import urlopen
import json

def test_join():
    players = {'one':'asdfg',
               'two':'asdfg',
               'six':'asdfg',
               'three': 'poiuy',
               'four': 'mnbvcx',
               'five':'zxcvb'}
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

def test_thrust():
    url = "http://localhost:7000/game/turn"
    data = {'auth':'asdfg', 
            'actions':[]}
    for id in json.loads(test_info_all())['objects']:
        action = {'obj_type':'ship', 
                  'ship_id': id, 
                  'command': 'thrust',
                  'args': { 'accel': (1, 1)}}
        data['actions'].append(action)
    return urlopen(url, json.dumps(data)).read()

if __name__ == '__main__':
    print test_join()
    print test_info()
    print test_info_all()
    print test_thrust()
