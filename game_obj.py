class GameObject(object):
	"""Base class for all game objects on the map since they need
	certain common info
	"""
	
	def __init__(self, game, position, owner):
		self.game = game
		self.position = position
		self.velocity = (0,0)
		self.direction = 0
		self.size = 1
		self.owner = owner
		self.alive = True

		# holds all events to be processed on turn handle
		self.events = []
		
		# holds results from turns to be returned to user
		# dict of lists accessed like results[turn]
		self.results = {0: []}
		
		# set methods used to true in this dict to prevent
		# double dipping
		self.methods_used = {}

	def step(self, dt):
		"""Timestep executed every turn.
		
		@param dt: whatever dt means
		"""
		
		vx, vy = self.velocity
		x, y = self.position
		self.position = (x + dt*vx, y + dt*vy)

	def handle_damage(self, damage_event):
		"""By default, do nothing.
		
		@param damage_event: whatever damage_events are
		"""
		
		pass

	def to_dict(self):
		"""Returns the current state in JSON serializable representation.
		
		"""
		
		state = {'obj_id': id(self),
				'owner': self.owner,
				'position':self.position,
				'alive': self.alive,
				'results':self.results[self.game.turn]
				}
		return state
