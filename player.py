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

	def add_object(self, obj):
		"""Add an object to the player's directory.
		@param obj: The object to add.
		"""
		objID = id(obj)
		if objID not in self.objects.keys():
			self.objects[objID] = obj
		return objID

if __name__ == "__main__":
	unittest.main()
