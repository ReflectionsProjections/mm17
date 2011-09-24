#! /usr/bin/env python
""" Constants used in ship.py  """
base_size = 10
base_health = 100
scan_range = 2000
weapon_range = 1000
weapon_strength = 100

max_velocity = 50
max_accel = 5

""" Constants used in asteroid.py """
asteroid_scale = 10  # asteroid.resources = size * asteroidScale
resource_pull = 1    # Ammount of resources pulled from factories each turn


if __name__ == '__main__':
	unittest.main()
