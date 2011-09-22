#! /usr/bin/env python
from urllib2 import urlopen

def test_join():
    players = {'one':'asdfg',
               'two':'asdfg',
               'six':'asdfg',
               'three': 'poiuy',
               'four': 'mnbvcx',
               'five':'zxcvb'}
    for name, auth in players.items():
        url = "http://localhost:7000/game/join?name="+name+"&auth="+auth
        print urlopen(url).read()

def test_info():
        url = "http://localhost:7000/game/info"
        print urlopen(url).read()

if __name__ == '__main__':
    test_join()
    test_info()
