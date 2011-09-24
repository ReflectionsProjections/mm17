from game_obj import GameObject
import Constants

# TODO: Fix gameobject to agree with this file and also documentation.
class Asteroid(GameObject):
	# XXX: this set of arguments based on the removal of owner in gameobject
	def __init__(self, game, position, size):
		super(Asteroid, self).__init__(game, position)
		self.size = size
		self.resources = size * Constants.asteroid_scale


	def pullResources():
		self.resources -= Constants.resource_pull

