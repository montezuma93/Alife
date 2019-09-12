#! /usr/bin/env python

import sys
import os
sys.path.append("alife")

# Default map
map_file = "RANDOM_MAP"
'''
if len(sys.argv) > 1:
    map_file = sys.argv[1]
'''
# Density of initial sprites
init_sprites = 0
'''
if len(sys.argv) > 2:
    init_sprites = int(sys.argv[2])
'''

from world import *
test_run_name = None
agent_string = None
if len(sys.argv) > 1:
    test_run_name = sys.argv[1]

if len(sys.argv) > 2:
    agent_string = sys.argv[2]
    with open(test_run_name + '.yml') as file:
        config_file = yaml.load(file)
        bugs = config_file['bugs']
        bugs[3] = sys.argv[2]
        log_file = config_file['log_file']
        log_file['name'] = test_run_name + ".csv"
        with open(test_run_name+'.yml', "w") as file:
            yaml.dump(config_file, file)
if len(sys.argv) > 2:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init()
world = World(map_file,init_sprites,test_run_name, agent_string)
