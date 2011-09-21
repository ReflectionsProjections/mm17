def handle_input(input, game):
    """Hadles incoming input from POST requests and passes 
    them to validators."""
    if 'auth' in input.keys():
        for player in game.players:
            if input['auth'] == player.auth_tokem:
                return validate_actions(game, player, input)
            else:
                return {'error':'bad auth token'}
    else:
        return {'error':'no auth token provided'}

def validate_actions(game, player, input):
    """Filter down to well-formed and legal actions. 
    Return a pair of a JSON description of the paring 
    results and a parsed representation of the actions"""
    if 'actions' not in input:
        return {'error': 'no actions provided'}
    results = []
    for action in actions:
        if action['obj_type'] == "ship":
            
            results.append(validate_ship_action(action))
        else:
            results.append({'error':'bad or no obj_type in action'})
    return results

def validate_ship_action(action, player, game):
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
        if 'accel' not in action['args'].keys():
          return {'error':'thrust requires accel arg'}
        elif not isinstance(action['args']['accel'], tuple):
          return {'error':'accel must be tuple'}
        else:
            accel = action['args']['accel']
            try:
                a, b = int(accel[0], accel[1])
            except:
                return {'error':'invalid accel values'}
            result = {'obj_id': action['ship_id'],
                      'method': action['command'],
                      'params': action['args']}
            game.actions[gam.turn][player].append(result)
            return {'success' : True}
    elif action['command'] == 'fire':
        if 'angle' not in action['args'].keys():
          return {'error':'fire requires angle arg'}
        else:
            angle = action['args']['angle']
            try:
                angle = int(angle)
            except:
                return {'error':'invalid angle value'}
            result = {'obj_id': action['ship_id'],
                      'method': action['command'],
                      'params': action['args']}
            game.actions[game.turn][player].append(result)
            return {'success' : True}
    else:
        return {'error':'invalid ship command'}
