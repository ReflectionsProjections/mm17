class GameObject(object):
	"""Base class for all game objects on the map since they need 
	certain common info"""
	def __init__(self, game, position, owner):
		self.game = game
		self.position = position
		self.velocity = (0,0)
		self.owner = owner
		self.alive = True

		# holds all events to be processed on turn handle
		self.events = []

		# holds results from turns to be returned to user
		# dict of lists accessed like results[turn]
		self.results = {0: []}


	def step(self, dt):
		vx, vy = self.velocity
		x, y = self.position
		self.position = (x + dt*vx, y + dt*vy)

	def get_state(self):
		state = {'obj_id': id(self),
			 'owner': self.owner,
			 'position':self.position,
			 'alive': self.alive,
			 'results':self.results[self.game.turn]
			 }
		return state

	def handle_damage(self, damage_event):
		"""By default, do nothing."""
		pass
