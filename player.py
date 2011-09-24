#! /usr/bin/env python
import unittest

class Player(object):
	def __init__(self, name, auth_token):
		"""Create a new player representation.
		@param name: The name of the new player
		@param auth_token: Authorization code for the payer (unique)
		"""
		self.name = name
		self.auth_token = auth_token
		self.alive = True
		self.objects = {}
		self.ships = {}
		self.bases = {}
		self.refineries = {}
		self.dicts = [self.ships,
					  self.bases,
					  self.refineries]

	def add_object(self, obj):
		"""Add an object to the player's directory.
		@param obj: The object to add.
		"""
		objID = id(obj)
		if objID not in self.objects.keys():
			self.objects[objID] = obj
		return objID

class PlayerTests(unittest.TestCase):
	def test_create(self):
		p = Player("Hello","world")
		self.assertTrue(p.name == "Hello")
		self.assertTrue(p.auth_token == "world")
		self.assertTrue(p.alive)
		self.assertTrue(len(p.objects) == 0)
	def test_add(self):
		p = Player("a","b")
		objects = []
		objects.append("hello")
		objects.append("test")
		for i in objects:
			p.add_object(i)
		self.assertTrue(len(p.objects) == 2)

if __name__ == "__main__":
	unittest.main()
