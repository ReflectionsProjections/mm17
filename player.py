class Player(object):
	def __init__(self, name, auth_token):
		self.name = name
		self.auth_token = auth_token
		self.alive = True
