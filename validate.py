#!/usr/bin/env python
import unittest
from numbers import Number

def handle_input(input, game):
	"""Handle POST request data and passes to validators.
	
	@param input: Dictionary of input values to handle
	@param game: XXX game instance
	"""
	if 'auth' in input.keys():
		if input['auth'] in game.players.keys():
			return validate_actions(game, game.players[input['auth']], input)
		else:
			return {'error':'bad auth token'}
	else:
		return {'error':'no auth token provided'}

def validate_actions(game, player, input):
	"""Validate actions requested by a player

	@param game: XXX game instance
	@param player: The player requesting these actions
	@param input: JSON actions to parse
	@return JSON dump of parse results
	"""

	if 'actions' not in input:
		return {'error': 'no actions provided'}
	results = []
	game.actions[game.turn][player] = []

	for action in input['actions']:
		if action['obj_type'] == "ship":
			results.append(validate_ship_action(action, player, game))
		else:
			results.append({'error':'bad or no obj_type in action'})

	return results

def validate_ship_action(action, player, game):
	"""Valide an action performed by a ship

	@param action: Action to validate
	@param player: The player that requested the action
	@param game: XXX game instance
	"""
	# make sure a ship action has all required keys
	attrs = ['command', 'ship_id', 'args']
	for attr in attrs:
		if attr not in action.keys():
			return {'error':'ship action requires a %s attribute' % attr}

	# attempt to coerce the ship_id to int
	try:
		ship_id = action['ship_id']
	except:
		return {'error':'invalid ship id'}

	# check if ship exiss
	if ship_id in game.game_map.ships.keys():
		ship = game.game_map.ships[ship_id]
	else:
		return {'error': 'ship does not exist'}

	# make sure the player owns the ship
	if ship.owner != player:
		return {'error':'not authenticated for that ship'}

	# check to see if ship is alive
	if ship.alive == False:
		return {'error':'ship has been destroyed'}

	# make sure args is a dict
	if not isinstance(action['args'], dict):
		return {'error':'args must be a dictionary'}

	# validate commands
	if action['command'] == 'thrust':
		if ship.methods_used['thrust']:
			return {'error':'thrust action already used'}

		if 'accel' not in action['args'].keys():
			return {'error':'thrust requires accel arg'}
		elif not isinstance(action['args']['accel'], list):
			return {'error':'accel must be list'}
		else:
			accel = action['args']['accel']

			try:
				a, b = accel[0], accel[1]
			except:
				return {'error':'invalid accel values'}

			result = {'obj_id': action['ship_id'],
					'method': action['command'],
					'params': action['args']}
			game.actions[game.turn][player].append(result)
			ship.methods_used['thrust'] = True

			return {'success' : True}

	elif action['command'] == 'fire':
		if ship.methods_used['fire']:
			return {'error':'fire action already used'}
		elif 'angle' not in action['args'].keys():
			return {'error':'fire requires angle arg'}
		else:
			angle = action['args']['angle']
			if not isinstance(angle, Number):
				return {'error':'angle must be int'}
			result = {'obj_id': action['ship_id'],
					'method': action['command'],
					'params': action['args']}
			game.actions[game.turn][player].append(result)
			ship.methods_used['fire'] = True

			return {'success' : True}
	else:
		return {'error':'invalid ship command'}

class UnitTests(unittest.TestCase):
	def test_main(self):
		print "hello world"
		self.assertTrue(True)

if __name__ == "__main__":
	unittest.main()
