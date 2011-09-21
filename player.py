class Player(object):
	def __init__(self, name, auth_token):
		self.name = name
		self.auth_token = auth_token
		self.alive = True
		self.objects = {}

	def add_object(self, object):
		"""Adds an object to the players's global object dictionary."""
		objID = id(object)
		if objID not in self.objects.keys():
			self.objects[objID] = object

		return objID
