#! /usr/bin/env python
""" Constants used in ship.py  """
ship_size = 10
ship_health = 300
scan_range = 2000
weapon_range = 1000
weapon_strength = 10
weapon_width = 75
max_velocity = 200
max_accel = 20

refinery_price = 2500
base_price = 5000

""" Constants used in asteroid.py """
asteroid_scale = 10  # asteroid.resources = size * asteroidScale
resource_pull = 3    # Ammount of resources pulled from factories each turn
refinery_health = 700
refinery_build_time = 50
""" Constants used in players.py """
score_constant = 1
start_resources = 5000
base_resource_pull = 1

""" Constants used in planet.py """
planet_scale = 10000
repair_percent = 0.10
build_radius = 15
ship_price = 1000
salvage_multiplier = 10
base_health = 5000
base_build_time = 100
""" Constants used in game.py """
x_range = range(-20000,20000,1000)
y_range = range(-20000,20000,1000)
player_starts = []
for x in range(len(x_range)):
	player_starts.append((x_range[x], y_range[x]))

""" Constants used in game.py """
x_range = range(-20000,20000,1000)
y_range = range(-20000,20000,1000)
player_starts = []
for x in range(len(x_range)):
	player_starts.append((x_range[x], y_range[x]))

""" Constants used in validate.py """
base_build_radius = 1500
base_salvage_radius = 1500
base_repair_radius = 1500

base_build_busy = 15
base_salvage_busy = 5
base_repair_busy = 10

ship_build_radius = 1500


if __name__ == '__main__':
	# No unit tests for constants
	pass
