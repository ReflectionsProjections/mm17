def validate(gamef, player, actions):
    """Filter down to well-formed and legal actions.
    Return a pair of a JSON description of the paring results,
    and a parsed representation of the actions"""
    valid = 0
    duplicate = 0
    wrong_owner = 0
    invalid_ship = 0
    malformed = 0
    
    thrust = {}
    fire = {}
    for a in actions:
        if not(hasattr(a,'command')) or \
                not(a['command'] in ['thrust','fire']) or \
                not(hasattr(a,'ship')):
            malformed += 1
        else:
            try:
                sid = int(a.ship)
            except ValueError:
                malformed += 1
            else:
                if sid not in self.game_map:
                    invalid_ship += 1
                elif not(self.game_map[sid].owner is player):
                    wrong_owner += 1
                else:
                    if a.command == 'thrust':
                        if sid in thrust:
                            duplicate += 1
                        else:
                            if not(hasattr(a,'thrust')) or \
                                    not(type(a.thrust) is list) or \
                                    len(a.thrust) != 2:
                                malformed += 1
                            else:
                                thrust[sid] = a.thrust
                                valid += 1
                    elif a.command == 'fire':
                        if sid in fire:
                            duplicate += 1
                        else:
                            if not(hasattr(a,'angle')) or \
                                    not (type(a.angle) in [float,int,long]):
                                malformed += 1
                            else:
                                fire[sid] = a.angle
                                valid += 1
                                self.actions[player] = {'thrust':thrust, 'fire':fire}

return {'valid':valid,
        'duplicate':duplicate,
        'wrong_owner':wrong_owner,
        'invalid_ship':invalid_ship,
        'malformed':malformed}


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
            game.actions[gam.turn][player].append(action)
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
            game.actions[gam.turn][player].append(action)
            return {'success' : True}
    else:
        return {'error':'invalid ship command'}

