#! /usr/bin/env python

import pygame
import random
import numpy as np
from functools import reduce
from prettytable import PrettyTable
import csv
import sys
import rope.base.astutils
import os
import re

from graphics import *
from objects import *
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
# For saving and loading agents from disk
import joblib, glob, time, datetime
# For loading config
import yaml
def get_conf(filename='conf.yml',section='world'):
    return yaml.load(open(filename))[section]

CONFIG_FILENAME='conf.yml'
cfg = get_conf(filename='conf.yml',section='objects')

# Parameters
TILE_SIZE = 64               # tile size (width and height, in pixels)
MAX_GRID_DETECTION = 100     # maximum number of objects that can be detected at once

class DrawGroup(pygame.sprite.Group):
    def draw(self, surface):
        for s in self.sprites():
            s.draw(surface)

def load_map(s):
    ''' load a map from a text file '''
    MAP = zeros((10,10),dtype=int)
    if s is "RANDOM_MAP":
        MAP = create_random_txt_for_map()
    elif s is not None and s is not "RANDOM_MAP":
        MAP = genfromtxt(s, delimiter = 1, dtype=str)     
    return MAP[1:-1,1:-1]

def create_random_txt_for_map():
    '''Construct that saves all possible tiles and its neighbours, can be extended and adjusted'''
    possible_terrains = {}
    possible_terrains[' '] = {'right': [']', ' ', 'C', '-'], 'bottom': [' ', 'v', '-', '&'], 'left': [' ', '[', 'D', '&', '\\'], 'top': [' ', '^', 'D', 'C']}
    possible_terrains['v'] = {'right': ['v', '&', '/', 'x'], 'bottom': ['~', '^', '+', 'L'], 'left': ['v', '-', '\\', '%'], 'top': [' ', '^', '+', 'L', 'C', 'D']}
    possible_terrains['^'] = {'right': ['^', 'L', 'D', '%'], 'bottom': [' ', 'v', '-', '&'], 'left': ['^', '+', 'C', 'x'], 'top': ['~', 'v', '\\', '/']}
    possible_terrains['['] = {'right': [']', ' ', '-', 'C'], 'bottom': ['[', '\\', 'D', '%'], 'left': [']', '~', 'L', '/'], 'top': ['[', '&', 'x', '+']}
    possible_terrains[']'] = {'right': ['[', '+', '~', '\\'], 'bottom': [']', '/', 'C', 'x'], 'left': ['[', 'L', ' ', '&', 'D'], 'top': [']', 'L', '-', '%']}
    possible_terrains['\\'] = {'right': ['&', '/', 'v', 'x'], 'bottom': ['+', '^', '~', 'L'], 'left': ['/', 'L', '~', ']'], 'top': ['+', '&', '[', 'x']}
    possible_terrains['/'] = {'right': ['\\', '~', '[', '+'], 'bottom': ['~', '^', 'L', '+'], 'left': ['\\', '-', 'v', '%'], 'top': ['-', 'L', ']', '\\', '%']}
    possible_terrains['+'] = {'right': ['^', 'L', 'D', '%'], 'bottom': ['[', '\\', 'D', '%'], 'left': ['L', ']', '~', '/'], 'top': ['~', '\\', '/', 'v'] }
    possible_terrains['L'] = {'right': ['+', '~', '[', '\\'], 'bottom': [']', '/', 'C', 'x'], 'left': ['+', 'C', '^', 'x'], 'top': ['~', '\\', '/', 'v']}
    possible_terrains['&'] = {'right': ['-', ' ', 'C', ']'], 'bottom': ['[', 'D', '\\', '%'], 'left': ['-', 'v', '\\', '%'], 'top': [' ', '^', 'D', 'C']}
    possible_terrains['D'] = {'right': [' ','-', ']', 'C'], 'bottom': [' ', '-', 'v', ' ', '&'], 'left': ['C', '^', '+', 'x'], 'top': ['&', '[', '+', 'x']}
    possible_terrains['C'] = {'right': ['L','^', 'D', '%'], 'bottom': ['&', '-', 'v', ' '], 'left': ['D', ' ', '&', '['], 'top': ['-', ']', 'L', '%']}
    possible_terrains['-'] = {'right': ['/', 'v', '&', 'x'], 'bottom': [']', '/', 'C', 'x'], 'left': ['&', 'D', ' ', '['], 'top': ['D', ' ', 'C', '^']}
    possible_terrains['~'] = {'right': ['~', '[', '\\', '+'], 'bottom': ['~', 'L', '^', '+'], 'left': [']', '/', 'L', '~'], 'top': ['~','v', '\\', '/']}
    possible_terrains['x'] = {'right': ['^', 'L', 'D', '%'], 'bottom': ['[', '\\', 'D', '%'], 'left': ['v', '\\', '-', '%'], 'top': [']', 'L', '-', '%']}
    possible_terrains['%'] = {'right': ['v', '/', '&', 'x'], 'bottom': [']', '/', 'C', 'x'], 'left': ['^', '+', 'C', 'x'], 'top': ['[', '+', '&', 'x']}
    possible_terrains['ALL'] = [' ', 'v', '^', '[', ']', '\\', '/', 'L', '&', 'D', 'C', '~', '-', '+', 'x', '%']
    
    '''Init Map'''
    row_size = 16
    column_size = 30
    MAP = np.empty([row_size, column_size],  dtype='str')

    '''Go through the Map and set tiles'''
    row = 0
    column = 0
    while row < row_size -1 or column < column_size - 1:
        need_restart = False
        left_choice = None
        top_choice = None
        first_row_choice = None
        first_column_choice = None

        '''Build the frame'''
        if(column == 0 or column == column_size - 1):
                MAP[row, column] = '|'
        if(row == 0 or row == row_size - 1):
            MAP[row,column] = '-'
        if((row == 0 or row == row_size-1) and (column == 0 or column == column_size - 1)):
            MAP[row,column] = '+'

        '''For every second row and column add a random terrain, based on the terrain on the left and on the top if available'''
        if((column % 2 == 1 and row % 2 == 1) and MAP[row, column] == ''):
            '''Last row need to fit first row in order to let the bugs walk through'''
            if row == row_size - 3:
                first_row_choice = MAP[1, column];
            if row >= 3:
                top_choice = MAP[row - 2, column]
            '''Last column need to fit first column in order to let the bugs walk through'''
            if column == column_size - 3:
                first_column_choice = MAP[row, 1]
            if column >= 3:
                left_choice = MAP[row, column -2]
            possible_right_terrain = possible_terrains[left_choice]['right'] if left_choice is not None else possible_terrains['ALL']
            possible_bottom_terrain = possible_terrains[top_choice]['bottom'] if top_choice is not None else possible_terrains['ALL']
            possible_last_row_terrain = possible_terrains[first_row_choice]['top'] if first_row_choice is not None else possible_terrains['ALL']
            possible_last_column_terrain = possible_terrains[first_column_choice]['left'] if first_column_choice is not None else possible_terrains['ALL']
            intersected_list = reduce(np.intersect1d, (possible_right_terrain, possible_bottom_terrain, possible_last_row_terrain, possible_last_column_terrain))
            '''If no possible tile was found, start again, otherwise choose a tile'''
            if len(intersected_list) > 0:
                if ' ' in intersected_list:
                    intersected_list = np.append(intersected_list, [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
                intersected_list = [' ']
                MAP[row, column] = random.choice(intersected_list)
            else:
                need_restart = True
        
        '''Add dots arround terrain tiles'''
        if((column % 2 == 0 or row % 2 == 0) and MAP[row, column] == '') :
            MAP[row, column] = '.'
        
        '''Calculate the next row, column to set a tile for. If need restart, init map again and start again'''
        if need_restart:
            row = 0
            column = 0
            MAP = np.empty([row_size, column_size],  dtype='str')
        else:
            if column < column_size -1  and row <= row_size -1 :
                column = column + 1
            elif column == column_size -1 and row <= row_size -1:
                column = 0
                row = row + 1
    return MAP

def get_conf(filename='conf.yml',section='world'):
    return yaml.load(open(filename))[section]

class World:
    """
        This is the world (environment) that objects exist in. 
    """

    def __init__(self,fname=None,init_sprites=0, test_run_name = None, agent_string = None):

        # Load the configuration
        cfg = get_conf(section='world')
        FPS = cfg['fps']

        map_codes = load_map(fname)                  # load the map
        self.N_ROWS = map_codes.shape[0]
        self.N_COLS = map_codes.shape[1]
        self.WIDTH = self.N_COLS * TILE_SIZE
        self.HEIGHT = self.N_ROWS * TILE_SIZE
        self.PLANT_TO_USE = ID_PLANT
        SCREEN = array([self.WIDTH, self.HEIGHT])


        sun = pygame.image.load("./img/Sun.png")
        sunrect = sun.get_rect()
        moon = pygame.image.load("./img/Moon.png")
        moonrect = moon.get_rect()
        step = 0

        ## GRID REGISTER and GRID COUNT 
        self.register = [[[None for l in range(MAX_GRID_DETECTION)] for k in range(self.N_ROWS)] for j in range(self.N_COLS)]
        #self.regcount = zeros(map_codes.shape,int) 
        self.regcount = zeros((self.N_COLS,self.N_ROWS),int) 

        ## INIT ##
        pygame.display.set_caption("ALife / Bug World")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))#, HWSURFACE|DOUBLEBUF)
        #scroll_offset = array([0, 0])
        pygame.mouse.set_visible(1)

        ## BACKGROUND ##
        from graphics import build_map_png as build_map
        background, self.terrain = build_map(self.screen.get_size(),self.N_COLS,self.N_ROWS,TILE_SIZE,map_codes)

        ## DISPLAY THE BACKGROUND ##
        self.screen.blit(background, [0, 0])
        pygame.display.flip()

        ## SPRITES ##
        self.allSprites = DrawGroup()
        self.creatures = pygame.sprite.Group()
        self.plants = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.stumps = pygame.sprite.Group()

        Creature.containers = self.allSprites, self.creatures
        Thing.containers = self.allSprites, self.plants

        self.clock = pygame.time.Clock()
        banner = get_banner("Start")
        
        # Some rocks and plants
        FACTOR = init_sprites
        #for i in range(int(self.N_ROWS*FACTOR/10*self.N_COLS)):
            #Thing(self.random_position(), mass=100+random.rand()*1000, ID=ID_ROCK)
        #for i in range(int(self.N_ROWS*FACTOR/5*self.N_COLS)):
            #Thing(self.random_position(), mass=100+random.rand()*cfg['max_plant_size'], ID=self.PLANT_TO_USE)

        # Get a list of the agents we may deploy 
        agents = None
        if test_run_name is not None:
            agents = get_conf(section='bugs', filename = test_run_name+'.yml').values()
        else:
            agents = get_conf(section='bugs').values()


        # Some animate creatures
        #for i in range(int(self.N_ROWS*FACTOR/10*self.N_COLS)):
        for c in range(len(agents)):
            p = self.random_position()
            for i in range(FACTOR):
                Creature(p + random.randn()*(TILE_SIZE/2), dna = list(agents)[c], ID=4+c)

        self.allSprites.clear(self.screen, background)

        ### Create proposition table
        self.create_proposition_table()
        ### Add plants and rocks and adjust params for Things and Livings based on random
        self.create_things_and_creatures(cfg['max_plant_size'], agents)
        if test_run_name is not None:
            self.agents_amount = 10
            self.create_agents(agents,  self.agents_amount, agent_string)
            ### Write configuration to file
            f = open(test_run_name + ".txt","a")
            x = PrettyTable()
            header = ["Plant Type"] + list(self.proposition_table_list["3"].keys()) 
            x.field_names = header
            for key, row in self.proposition_table_list.items():
                row_to_add = [key] + list(row.values())     
                x.add_row(row_to_add)
            f.write(x.get_string())
            f.write("\r\n")

            x = PrettyTable()
            header = ["Plant Type"] + list(self.available_proposition_table_list["3"].keys()) 
            x.field_names = header
            for key, row in self.available_proposition_table_list.items():
                row_to_add = [key] + list(row.values())     
                x.add_row(row_to_add)
            f.write(x.get_string())
            f.write("\r\n")

            
            f.close()

            header = ["AgentID", "Operation", "Result"]
            csv_file = open(test_run_name + ".csv", "w")
            writer = csv.DictWriter(csv_file, fieldnames=header,delimiter =";",lineterminator='\n',)
            writer.writeheader()
            csv_file.close()
        else:
            ### Write configuration to file
            f = open("agents.txt","w")
            x = PrettyTable()
            header = ["Plant Type"] + list(self.proposition_table_list["3"].keys()) 
            x.field_names = header
            for key, row in self.proposition_table_list.items():
                row_to_add = [key] + list(row.values())     
                x.add_row(row_to_add)
            f.write(x.get_string())
            f.write("\r\n")


            x = PrettyTable()
            header = ["Plant Type"] + list(self.available_proposition_table_list["3"].keys()) 
            x.field_names = header
            for key, row in self.available_proposition_table_list.items():
                row_to_add = [key] + list(row.values())     
                x.add_row(row_to_add)
            f.write(x.get_string())
            f.write("\r\n")

            f.close()

            header = ["AgentID", "Operation", "Result"]
            csv_file = open("agents.csv", "w")
            writer = csv.DictWriter(csv_file, fieldnames=header,delimiter =";",lineterminator='\n',)
            writer.writeheader()
            csv_file.close()

        ## MAIN LOOP ##
        sel_obj = None 
        GRAPHICS_ON = True
        GRID_ON = False
        self.FPS = FPS
        clock = pygame.time.Clock()
        timer = 0
        dt = 0
        self.IS_DAY_TIME = True
        day_timer = 0
        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == pygame.KEYUP:
                    if sel_obj is not None:
                        sel_obj.selected = array([-0.0,0.])
                if event.type == pygame.KEYDOWN:
                    if sel_obj is not None:
                        # Human intervention in selected agent
                        if event.key == pygame.K_UP:
                            sel_obj.selected = array([-0.0,3.])
                        elif event.key == pygame.K_DOWN:
                            sel_obj.selected = array([-0.0,5.1])
                        if event.key == pygame.K_RIGHT:
                            sel_obj.selected = array([0.1,0.])
                        elif event.key == pygame.K_LEFT:
                            sel_obj.selected = array([-0.1,0.])
                        # TODO Restore control to RL agent later
                    if event.key == pygame.K_g:
                        GRAPHICS_ON = (GRAPHICS_ON != True)
                    elif event.key == pygame.K_d:
                        GRID_ON = (GRID_ON != True)
                    #elif event.key == pygame.K_e:
                    #    # TEST
                    #    scroll_offset = scroll_offset - TILE_SIZE
                    #    self.screen.blit(background, [0, 0])
                    #elif event.key == pygame.K_u:
                    #    # TEST
                    #    scroll_offset = scroll_offset + TILE_SIZE
                    #    self.screen.blit(background, [0, 0])
                    elif event.key == pygame.K_s and sel_obj is not None:
                        # TODO FIX
                        print("[Error] Functionality currently broken ...")
                        sel_obj.brain.save("./dat/dna/", "./dat/log/")
                    elif event.key == pygame.K_l:
                        # TODO FIX
                        print("[Error] Functionality currently broken ...")
                        #for filename in glob.glob('./dat/dna/*.dat'):
                        #    brain = pickle.load(open(filename, "rb"))
                        #    meta_data = filename.split(".")
                        #    ID = int(meta_data[2])
                        #    params = (200,200,int(meta_data[5]),ID,ID-1)
                        #    if ID == ID_OTHER:
                        #        params = (200,400,int(meta_data[5]),ID,ID-1)
                        #    print("Loaded Creature ID=%d from %s ..." % (params[3],filename))
                        #    Creature(array(pygame.mouse.get_pos()+random.randn(2)*TILE_SIZE),dna=brain, energy = params[0], ID = params[3])
                    elif event.key == pygame.K_PLUS:
                        self.FPS = self.FPS + 50
                        print("FPS: %d" % self.FPS)
                    elif event.key == pygame.K_MINUS:
                        self.FPS = self.FPS - 50
                        print("FPS: %d" % self.FPS)
                    elif event.key == pygame.K_COMMA:
                        with open(CONFIG_FILENAME) as file:
                            config_file = yaml.load(file)
                            growth_rate = config_file['world']['growth_rate']['ID_' + str(self.PLANT_TO_USE)]
                            config_file['world']['growth_rate']['ID_' + str(self.PLANT_TO_USE)] = growth_rate + 100             
                            with open(CONFIG_FILENAME, "w") as file:
                                yaml.dump(config_file, file)
                            print("Lower energy influx (new plant every %d ticks)" % (growth_rate + 100))
                    elif event.key == pygame.K_PERIOD:
                        with open(CONFIG_FILENAME) as file:
                            config_file = yaml.load(file)
                            growth_rate = config_file['world']['growth_rate']['ID_' + str(self.PLANT_TO_USE)]
                            config_file['world']['growth_rate']['ID_' + str(self.PLANT_TO_USE)] = growth_rate - 100.10             
                            with open(CONFIG_FILENAME, "w") as file:
                                yaml.dump(config_file, file)
                        print("Higher energy influx (new plant every %d ticks)" % (growth_rate - 100.10))
                    elif event.key == pygame.K_1:
                        print("New Rock")
                        Thing(array(pygame.mouse.get_pos()),mass=500, ID=ID_ROCK)
                    elif event.key == pygame.K_2:
                        print("New Tree Trunk")
                        Thing(array(pygame.mouse.get_pos()),mass=500, ID=ID_TREE_TRUNK)
                    elif event.key == pygame.K_3:
                        if timer == 0:
                            timer = 0.001
                        elif timer < 0.25:
                            print('Double click -> Changing plant kind')
                            if self.PLANT_TO_USE == ID_PLANT:
                                 self.PLANT_TO_USE = ID_PLANT_ORANGE
                            elif self.PLANT_TO_USE == ID_PLANT_ORANGE:
                                self.PLANT_TO_USE = ID_PLANT_PURPLE
                            elif self.PLANT_TO_USE == ID_PLANT_PURPLE:
                                self.PLANT_TO_USE = ID_PLANT_BLUE
                            else:
                                self.PLANT_TO_USE = ID_PLANT
                            timer = 0
                    elif event.key == pygame.K_4 and len(agents) >= (4-4):
                        print("New Agent")
                        Creature(array(pygame.mouse.get_pos()), dna = list(agents)[2], ID = 4)
                    elif event.key == pygame.K_5 and len(agents) >= (5-4):
                        print("New Agent")
                        Creature(array(pygame.mouse.get_pos()), dna = list(agents)[5-4], ID = 5)
                    elif event.key == pygame.K_6 and len(agents) >= (6-4):
                        print("New Agent")
                        Creature(array(pygame.mouse.get_pos()), dna = list(agents)[6-4], ID = 6)
                    elif event.key == pygame.K_7 and len(agents) >= (7-4):
                        print("New Agent")
                        Creature(array(pygame.mouse.get_pos()), dna = list(agents)[7-4], ID = 7)
                    elif event.key == pygame.K_8 and len(agents) >= (8-4):
                        print("New Agent")
                        Creature(array(pygame.mouse.get_pos()), dna = list(agents)[8-4], ID = 8)
                    elif event.key == pygame.K_h:
                        print("=== HELP ===")
                        dic = ["VOID", "ROCK", "MISC", "BUG1", "BUG2", "BUG3"]
                        print(dic)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("Click")
                    sel_obj = self.quick_collision(pygame.mouse.get_pos())
                    print(sel_obj)
            
            if timer != 0:
                timer += dt
                if timer >= 0.25:
                    Thing(array(pygame.mouse.get_pos()), mass=100+random.rand()*cfg['max_plant_size'], ID=self.PLANT_TO_USE)
                    print("New Plant")
                    timer = 0

            dt = clock.tick(60) /1000
            # Make sure there is a constant flow of resources/energy into the system
            step = step + 1

            # To let plant grow consistently
            '''
            for plant_type in (ID_PLANT, ID_PLANT_ORANGE, ID_PLANT_PURPLE, ID_PLANT_BLUE):
                if step % get_conf(section='world')['growth_rate']['ID_' + str(plant_type)] == 0:
                    p = self.random_position()
                    if p is not None and len(self.plants) < 1000:
                        Thing(p, mass=100+random.rand()*cfg['max_plant_size'], ID=plant_type)
                    banner = get_banner("t=%d; %d bugs" % (step,len(self.creatures)))
                    
            '''
            
            day_timer = day_timer + 1
            if day_timer >= 800:
                #print("Time step %d; %d bugs alive" % (step,len(self.creatures)))
                self.IS_DAY_TIME = not self.IS_DAY_TIME
                day_timer = 0

            # Reset reg-counts and Register all sprites
            self.regcount = zeros((self.N_COLS,self.N_ROWS),int) 
            for r in self.allSprites:
                self.add_to_register(r)

            # Routine
            for r in self.allSprites:
                r.live(self)
            # Just for Game Results
            if test_run_name is not None:
                if self.evidence_interpreation == 'EVIDENCE':
                    if len(self.creatures) == 0 or step > 10000:
                        self.create_results(test_run_name, self.creatures, step)              
                        sys.exit()
                else:
                    if len(self.creatures) == 0 or step > 2000:
                        self.create_results(test_run_name, self.creatures, step)              
                        sys.exit()

            if GRAPHICS_ON:

                # Update sprites
                self.allSprites.update()
                # Draw the background
                # @TODO redraw only the visible/active tiles; the ones with moving sprites ontop of them
                self.screen.blit(background, [0,0]) #[scroll_offset[0], scroll_offset[1], scroll_offset[0] + 100, scroll_offset[1] + 100])
                # Draw the grid
                if GRID_ON:
                    self.screen.blit(banner,[10,10])
                    # GRID ON
                    for l in range(0,self.N_ROWS*TILE_SIZE,TILE_SIZE):
                        pygame.draw.line(self.screen, COLOR_WHITE, [0, l], [SCREEN[0],l], 1)
                    for l in range(0,self.N_COLS*TILE_SIZE,TILE_SIZE):
                        pygame.draw.line(self.screen, COLOR_WHITE, [l, 0], [l,SCREEN[1]], 1)
                # Draw the sprites
                # @TODO draw only the dirty sprites (the ones that have moved since last time)
                rects = self.allSprites.draw(self.screen)
                # Draw the selected sprite
                if sel_obj is not None:
                    sel_obj.draw_selected(self.screen)
                # Display
                pygame.display.update(rects)
                if test_run_name is None:
                    if self.IS_DAY_TIME:
                        self.screen.blit(sun, sunrect)
                        pygame.display.flip()
                    else:
                        self.screen.blit(moon, moonrect)
                        pygame.display.flip()
                        '''
                        darken_percent = .10
                        dark = pygame.Surface(self.screen.get_size()).convert_alpha()
                        dark.fill((0, 0, 0, darken_percent*255))
                        self.screen.blit(dark, (0, 0))
                        '''
                else:
                    pygame.display.flip()
                    #pygame.time.delay(self.FPS)

    def create_things_and_creatures(self, max_plant_size, agents):
        found_combination = []
        positions_used_plants = []
        for thing_type in (ID_PLANT, ID_PLANT_ORANGE, ID_PLANT_PURPLE, ID_PLANT_BLUE):
            for i in range(random.randint(2,8)):
                random_position = self.random_position(positions_used_plants = positions_used_plants)
                if random_position is not None:
                    positions_used_plants.append((thing_type, random_position))
                    found_combination.append([thing_type])
                    Thing(random_position, mass=350, ID=thing_type)
                #Add rocks and tree trunks

        thing_type = ID_ROCK
        positions_used_objects = []
        for i in range(random.randint(7,25)):
            random_position = self.random_position(positions_used_plants = positions_used_plants, positions_used_objects = positions_used_objects)
            if random_position is not None:
                found_combination[random_position[0]].append(thing_type)
                positions_used_objects.append(random_position[1])
                Thing(random_position[1], mass=350, ID=thing_type)
        thing_type = ID_TREE_TRUNK
        positions_used_objects = []
        for i in range(random.randint(10,25)):
            random_position = self.random_position(positions_used_plants = positions_used_plants, positions_used_objects = positions_used_objects)
            if random_position is not None:
                found_combination[random_position[0]].append(thing_type)
                positions_used_objects.append(random_position[1])
                Thing(random_position[1], mass=350, ID=thing_type)
        
        possible_combinations = []
        for combination in found_combination:
            if combination not in possible_combinations:
                possible_combinations.append(combination)
        
        self.create_availableproposition_table(possible_combinations)

        for r in self.allSprites:
            self.add_to_register(r)
        
    def create_agents(self, agents, amount, agent_string):
        for i in range(amount):
            p = self.random_position()
            Creature(p + random.randn()*(TILE_SIZE/2), dna = list(agents)[2], ID=4)
        if agent_string is not None:
            if 'RANKING' in agent_string:
                self.evidence_interpreation = 'RANKING'
            elif 'PROBABILITY' in agent_string:
                self.evidence_interpreation = 'PROBABILITY'
            elif 'EVIDENCE' in agent_string:
                self.evidence_interpreation = 'EVIDENCE'


    def create_proposition_table(self):
        self.proposition_table_list = {}
        plants_toxicity = ['X', '!X']
        for plant_id in PLANT_IDS:
            self.proposition_table_list[str(plant_id)] = {
                'day_1': random.choice(plants_toxicity),
                'day_2': random.choice(plants_toxicity),
                'day_1_2': random.choice(plants_toxicity),
                'day_': random.choice(plants_toxicity),
                'night_1': random.choice(plants_toxicity),
                'night_2': random.choice(plants_toxicity),
                'night_1_2': random.choice(plants_toxicity),
                'night_': random.choice(plants_toxicity)
            }      

    def create_availableproposition_table(self, available_propositions):
        self.available_proposition_table_list = {}
        for plant_id in PLANT_IDS:
            self.available_proposition_table_list[str(plant_id)] = {
                'day_1': 0,
                'day_2': 0,
                'day_1_2': 0,
                'day_': 0,
                'night_1': 0,
                'night_2': 0,
                'night_1_2': 0,
                'night_': 0
            }   

        for available_proposition in available_propositions:
            if len(available_proposition) ==1:
                self.available_proposition_table_list[str(available_proposition[0])]['day_'] = 1
                self.available_proposition_table_list[str(available_proposition[0])]['night_'] = 1
            elif len(available_proposition) ==2:
                for proposition in available_proposition:
                    if proposition == 1:
                        self.available_proposition_table_list[str(available_proposition[0])]['day_1'] = 1
                        self.available_proposition_table_list[str(available_proposition[0])]['night_1'] = 1
                    if proposition == 2:
                        self.available_proposition_table_list[str(available_proposition[0])]['day_2'] = 1
                        self.available_proposition_table_list[str(available_proposition[0])]['night_2'] = 1
            else:           
                self.available_proposition_table_list[str(available_proposition[0])]['day_1_2'] = 1
                self.available_proposition_table_list[str(available_proposition[0])]['night_1_2'] = 1


    def random_position(self, on_empty=False, positions_used_plants = [], positions_used_objects = None):
        ''' Find a random position somewhere on the screen over land tiles
            (if specified -- only on an empty tile) '''
        # For adding things like rock and tree, Want them close to a plant
        if positions_used_objects is not None:
            distance_is_wrong = False
            which_to_use = np.random.randint(0 , len(positions_used_plants)-1)
            point = positions_used_plants[which_to_use][1]
            plant_type_use = positions_used_plants[which_to_use][0] 
            calculated_point_x = np.random.uniform(point[0] -20 , point[0] +20)
            calculated_point_y = np.random.uniform(point[1] -20 , point[1] +20)
            distance_to_plant = calculate_distance(calculated_point_x, calculated_point_y, point[0], point[1])
            for point_of_object  in positions_used_objects:
                distance_to_object = calculate_distance(calculated_point_x, calculated_point_y, point_of_object[0], point_of_object[1])     
                if distance_to_object < 50 or distance_to_plant > 25 or distance_to_plant < 10:
                    distance_is_wrong = True
            if not distance_is_wrong:
                return (which_to_use, array([calculated_point_x, calculated_point_y]))
        # For all other case, for adding plants
        else:
            j_list = list(range(self.terrain.shape[0]))
            random.shuffle(j_list)
            k_list = list(range(self.terrain.shape[1]))
            random.shuffle(k_list)
            for j in j_list:
                for k in k_list:
                    if not (self.terrain[j,k] > 0) and not (self.regcount[k,j] > 0 and on_empty):
                        calculated_position = self.grid2pos((k,j)) + random.rand(2) * TILE_SIZE - TILE_SIZE*0.5
                        distance_is_wrong = False
                        for point in positions_used_plants:
                            distance = calculate_distance(point[1][0], point[1][1], calculated_position[0], calculated_position[1])
                            if distance < 250:
                                distance_is_wrong = True
                        if not distance_is_wrong:
                            return calculated_position
        # There are no empty tiles
        # print("Warning: No empty tiles to place stuff on")
        return None
        return self.random_position(on_empty=False)

    def grid2pos(self,grid_square):
        ''' Grid reference to point (mid-point of the grid-square) '''
        x,y = grid_square
        px = x * float(TILE_SIZE) + 0.5 * TILE_SIZE
        py = y * float(TILE_SIZE) + 0.5 * TILE_SIZE
        return array([px,py])

    def pos2grid(self,p):
        ''' Position (point) to grid reference ''' 
        # N.B. we could also wrap around 
        rx = clip(int(p[0]/TILE_SIZE),0,self.N_COLS-1)
        ry = clip(int(p[1]/TILE_SIZE),0,self.N_ROWS-1)
        return rx,ry

    def distance_to_wall(self,p,my_tile,ne_tile):
        ''' Return the closest point on the wall to point 'p'.

            p: 
                my current position
            my_tile: 
                the tile I'm in
            ne_tile: 
                neighboring tile 

            1. check if the tile is vertically or horizontally aligned with our 
                tile (or neither)
            2. return the distance to the edfe of the tile

            Return: 
                the distance to the neighbouring tile
        '''

        p_ne = self.grid2pos(ne_tile)

        if ne_tile[0] == my_tile[0]:
            # Horizontally aligned
            return abs(p_ne[0] - p[0]) - TILE_SIZE * 0.5
        elif ne_tile[1] == my_tile[1]:
            # Vertically aligned
            return abs(p_ne[1] - p[1]) - TILE_SIZE * 0.5
        else:
            # Neither (diagonal to us)
            p_diff = abs(p_ne - p) - TILE_SIZE * 0.5
            return sqrt(dot(p_diff,p_diff))

    def add_to_register(self, sprite):
        '''
            Register this sprite.
        '''
        x,y = self.pos2grid(sprite.pos)
        c = self.regcount[x,y] 
        if c < MAX_GRID_DETECTION:
            self.register[x][y][c] = sprite
            self.regcount[x,y] = c + 1
        else:
            print("WARNING: Grid full, not registering!")
            exit(1)

    def quick_collision(self, s_point): 
        '''
            Check collisions of some point s_point.
            Return the object below it, or None if there is none.
        '''
        g_x, g_y = self.pos2grid(s_point)
        things = self.register[g_x][g_y]
        for i in range(self.regcount[g_x,g_y]):
            if overlap(s_point,1,things[i].pos,things[i].radius) > 0.:
                return things[i]
        return None

    def collision_to_vision(self, s_point, s_radius, excl=None, s_collision_radius=1):
        '''
            Check collisions of some circle s (defined by s_point and s_radius) in the world.

            The point and radius specified do not necessarily have to be a sprite.

            Parameters
            ----------

            s_point : tuple (x,y)
                the centre point of the object of interest

            s_radius : float
                the radius of the object

            excl : Thing
                exclude this object from the search

            s_collision_radius : float
                The true radius (not necessarily the detection radius) -- to detect actual collisions
                This is normally an 'inner radius' (detection radius > body radius)
                Being 1 as default, it means a collision only when the other object touches our centre point.


            Returns
            -------
            
            A tuple (color,object,type) where 
                vision : the [R,G,B] color of the resulting collisions 
                thing : the Thing that we collided with (None if terrain)
                type : the centre point of terrain tile we collided with 
                        (and None if not collided with terrain)

            Notes
            -----

            TODO: if touching object (inverse distance = 1, then all other objects are ignored)
            TODO: even if touching, the antennae should give mixed colours back
                (maybe need a special option to this function for that -- and some refactoring)

        '''
        TOUCH_THRESHOLD = 0.9        # maximum visual field occupied by color if not actually touching anything

        # We are currently in grid square (x,y)
        grid_x, grid_y = self.pos2grid(s_point)

        # By default, we don't see anything (pure blackness)
        vision = array([0.,0.,0.,])
        # .. and we don't collide with anything.
        thing = None

        # Check collision with current tile
        if self.terrain[grid_y,grid_x] > 0:
            # We are colliding with (i.e., we are over) impassable terrain
            vision = array([1.,1.,1.,])
            return vision, None, self.grid2pos((grid_x,grid_y))

        # Check collisions with objects in current and neighbouring tiles  
        for i in [-1,0,+1]:
            g_x = (grid_x + i) % self.N_COLS
            for j in [-1,0,+1]:
                g_y = (grid_y + j) % self.N_ROWS

                # If we are looking at terrain tile ...
                if i != 0 and j != 0 and self.terrain[g_y,g_x] > 0:
                    # ... check proximity to it.

                    # (distance of my outer self to the wall) 
                    d = self.distance_to_wall(s_point,(grid_x,grid_y),(g_x,g_y)) - s_collision_radius
                    # (max distance that I can be to the wall while still touching it) 
                    d_max = s_radius - s_collision_radius
                    if d < d_max: 
                        # We are touching the wall
                        vision = vision + object2rgb(excl.ID,ID_ROCK) * get_intensity((d_max - d) / d_max, float(TILE_SIZE)/s_collision_radius)

                # Check for collisions with other objects in this tile
                things = self.register[g_x][g_y]
                for i in range(self.regcount[g_x,g_y]):
                    # If this object is not me, ...
                    if things[i] != excl:

                        # ... how much overlap with the this thing?
                        olap = overlap(s_point,s_radius,things[i].pos,things[i].radius)

                        if olap > 0.:

                            # If the overlap greater than the outer + inner radius ...
                            if olap > (s_radius + s_collision_radius):
                                # it means we are completely overlapped by this object, return it now
                                if things[i].ID != 1 and things[i].ID != 2:
                                    return object2rgb(excl.ID,things[i].ID), things[i], None

                            # distance of the outer - inner radius
                            d = (s_radius - s_collision_radius)

                            # If the overlap is greater than the (outer - inner) radius ...
                            if olap > d:
                                # it means the thing is touching us, save it but don't return yet
                                if things[i].ID != 1 and things[i].ID != 2:
                                    thing = things[i]
                                    vision = vision + object2rgb(excl.ID,things[i].ID) * get_intensity(1., float(things[i].radius)/s_collision_radius)

                            # Otherwise ... (if the overlap is greater than 0, but not touching or covering us)
                            else:
                                # it means the object is in visual range, so we add the relevant intensity to our 'vision'
                                # N.B. max vision reached when touching collision radius!
                                vision = vision + object2rgb(excl.ID,things[i].ID) * get_intensity(olap / d, float(things[i].radius)/s_collision_radius)

        # If we get this far, we are not touching anything ..
        if thing is not None:
            vision = clip(vision,0.0,1.) 
        else:
            # (we should only reach 1.0 if actually touching some thing -- even if visual field is overwhelmed)
            # TODO could be relative, sigmoid/logarithmic, gaussian ?
            vision = clip(vision,0.0,TOUCH_THRESHOLD) 
        return vision, thing, None


    
    def create_results(self, test_run_name, creatures, step):
        # Game Over -> Get Results
        with open(test_run_name + '.csv', "r", encoding="utf-8", errors="ignore") as scraped:
            reader = csv.reader(scraped, delimiter=';')
            agents = {}
            for row in reader:
                if row:  # avoid blank lines
                    if row[0] in agents:
                        if row[2] == "nontoxic":
                            agents[row[0]]["nontoxic"] = agents[row[0]]["nontoxic"] + 1
                        elif row[2] == "toxic":
                            agents[row[0]]["toxic"] = agents[row[0]]["toxic"] + 1
                        elif row[1] == "Belief":
                            agents[row[0]]["Belief"] = row[2]
                    else:
                        if row[2] == "nontoxic":
                            agents[row[0]] = {"nontoxic":1, "toxic":0, "Belief": ""}
                        elif row[2] == "toxic":
                            agents[row[0]] = {"nontoxic":0, "toxic":1, "Belief": ""}
                        elif row[1] == "Belief":
                            agents[row[0]] = {"nontoxic":0, "toxic":1, "Belief": row[2]}
        scraped.close()

        new_created = False
        last_row = 0
        if not os.path.isfile('./' + test_run_name + '-results.csv'):
            header = ["RunId" ,"Step", "Agent", "ResultType", "Result"]
            csv_file = open(test_run_name + "-results.csv", "w")
            writer = csv.DictWriter(csv_file, fieldnames=header,delimiter =";",lineterminator='\n',)
            writer.writeheader()
            csv_file.close()
            new_created = True
        if not new_created:
            with open(test_run_name + '-results.csv', "r", encoding="utf-8", errors="ignore") as scraped:
                reader = csv.reader(scraped, delimiter=';')
                for row in reader:
                    if row:  # avoid blank lines
                        last_row = row[0]
            scraped.close
        next_run = str(int(last_row) + 1)
        row_to_append = []
        average_precission_X = 0
        average_precission_notX = 0
        average_recall_X = 0
        average_recall_notX = 0
        average_positive_reward = 0
        average_negative_reward = 0
        average_positive_negative_reward_ratio = 0

        for agent, value in agents.items():
            average_positive_reward =average_positive_reward + value["nontoxic"]
            average_negative_reward =average_negative_reward + value["toxic"]

            row_to_append.append([next_run, step, agent, "RewardPos", value["nontoxic"]])
            row_to_append.append([next_run, step, agent, "RewardNeg",  value["toxic"]])

            belief = value["Belief"].split("#")
            amount_of_true_negatives = 0
            amount_of_true_positives = 0
            amount_of_false_positives = 0
            amount_of_false_negatives = 0
            
            amount_of_available_propositions = 0
            amount_of_positives = 0
            amount_of_negatives = 0
            for color in self.available_proposition_table_list:
                for entry, available in self.available_proposition_table_list[color].items():
                    if available == 1:
                        amount_of_available_propositions = amount_of_available_propositions + 1
                        value = self.proposition_table_list[color][entry]
                        needs_to_contain = []
                        not_needs_to_contain = []
                        if color == "3":
                            needs_to_contain.append("GREEN") 
                        elif color == "31":
                            needs_to_contain.append("ORANGE") 
                        elif color == "32":
                            needs_to_contain.append("PURPLE") 
                        elif color == "33":
                            needs_to_contain.append("BLUE") 
                        if "1" in entry:
                            needs_to_contain.append("ROCK")
                        else:
                            not_needs_to_contain.append("ROCK")
                        if "2" in entry:
                            needs_to_contain.append("TREE")
                        else:
                            not_needs_to_contain.append("TREE")
                        if "day" in entry:
                            needs_to_contain.append("DAY")
                            not_needs_to_contain.append("!DAY")
                        if "night" in entry:
                            needs_to_contain.append("!DAY")
                        evidence_for_toxic = None
                        evidence_for_non_toxic = None
                        if self.evidence_interpreation == "EVIDENCE":
                            evidence_for_non_toxic = 0
                            evidence_for_toxic = 0
                        for sentence in belief:
                            if self.evidence_interpreation != "EVIDENCE":
                                if all([x in sentence for x in needs_to_contain]) and all([x not in sentence for x in not_needs_to_contain]):
                                    if "nontoxic" in sentence:
                                        splited = sentence.split("evidence: ")
                                        evidence_for_non_toxic = splited[1]
                                        evidence_for_non_toxic = float(evidence_for_non_toxic)
                                    else:
                                        splited = sentence.split("evidence: ")
                                        evidence_for_toxic = splited[1]
                                        evidence_for_toxic = float(evidence_for_toxic)
                            else:
                                or_sentences = re.compile("\sv\s").split(sentence)
                                for or_sentence in or_sentences:
                                    if all([x in sentence for x in needs_to_contain]) and all([x not in sentence for x in not_needs_to_contain]):
                                        if "nontoxic" in or_sentence:
                                            splited = sentence.split("evidence: ")
                                            evidence_for_non_toxic_part = splited[1]
                                            evidence_for_non_toxic = evidence_for_non_toxic + float(evidence_for_non_toxic_part)
                                        else:
                                            splited = sentence.split("evidence: ")
                                            evidence_for_toxic_part = splited[1]
                                            evidence_for_toxic = evidence_for_toxic+ float(evidence_for_toxic_part)

                        if value == "X":
                            amount_of_positives = amount_of_positives +1
                            if self.evidence_interpreation == "RANKING":
                                if evidence_for_toxic < evidence_for_non_toxic:
                                    amount_of_true_positives = amount_of_true_positives + 1
                                elif evidence_for_toxic > evidence_for_non_toxic:
                                    amount_of_false_positives = amount_of_false_positives + 1
                            else:
                                evidence_for_toxic = evidence_for_toxic if evidence_for_toxic is not None else 0
                                evidence_for_non_toxic = evidence_for_non_toxic if evidence_for_non_toxic is not None else 0
                                if evidence_for_toxic > evidence_for_non_toxic:
                                    amount_of_true_positives = amount_of_true_positives + 1
                                elif evidence_for_toxic < evidence_for_non_toxic:
                                    amount_of_false_positives = amount_of_false_positives + 1
                        elif value == "!X":
                            amount_of_negatives = amount_of_negatives +1
                            if self.evidence_interpreation == "RANKING":
                                if evidence_for_toxic > evidence_for_non_toxic:
                                    amount_of_true_negatives = amount_of_true_negatives + 1
                                elif evidence_for_toxic < evidence_for_non_toxic:
                                    amount_of_false_negatives = amount_of_false_negatives + 1
                            else:
                                evidence_for_toxic = evidence_for_toxic if evidence_for_toxic is not None else 0
                                evidence_for_non_toxic = evidence_for_non_toxic if evidence_for_non_toxic is not None else 0
                                if evidence_for_toxic < evidence_for_non_toxic:
                                    amount_of_true_negatives = amount_of_true_negatives + 1
                                elif evidence_for_toxic > evidence_for_non_toxic:
                                    amount_of_false_negatives = amount_of_false_negatives + 1
            
            row_to_append.append([next_run, step, agent, "AmountOfProposition",  amount_of_available_propositions])
            row_to_append.append([next_run, step, agent, "AmountOfPositivesProposition",  amount_of_positives])
            row_to_append.append([next_run, step, agent, "AmountOfNegativesProposition",  amount_of_negatives])

            row_to_append.append([next_run, step, agent, "AmountOfRightPositivesProposition",  amount_of_true_positives])
            row_to_append.append([next_run, step, agent, "AmountOfWrongPositivesProposition", amount_of_false_positives])
            row_to_append.append([next_run, step, agent, "AmountOfRightNegativesProposition", amount_of_true_negatives])
            row_to_append.append([next_run,step, agent, "AmountOfWrongNegativesProposition", amount_of_false_negatives])

            precission_X = amount_of_true_positives/(amount_of_true_positives+amount_of_false_positives) if amount_of_true_positives != 0 or amount_of_false_positives != 0 else 0
            average_precission_X = average_precission_X + precission_X
            precission_notX =  amount_of_true_negatives/(amount_of_true_negatives+amount_of_false_negatives) if amount_of_true_negatives != 0 or amount_of_false_negatives != 0 else 0
            average_precission_notX = average_precission_notX + precission_notX
            recall_X = amount_of_true_positives/(amount_of_true_positives+amount_of_false_negatives) if amount_of_true_positives != 0  or amount_of_false_negatives != 0 else 0
            average_recall_X = average_recall_X + recall_X
            recall_notX = amount_of_true_negatives/(amount_of_true_negatives+amount_of_false_positives) if amount_of_true_negatives != 0 or  amount_of_false_positives != 0 else 0
            average_recall_notX = average_recall_notX + recall_notX

            row_to_append.append([next_run, step, agent, "Precission_X",  precission_X])
            row_to_append.append([next_run, step, agent, "Precission_!X",precission_notX])
            row_to_append.append([next_run, step, agent, "Recall_X",recall_X])
            row_to_append.append([next_run,step, agent, "Recall_!X", recall_notX])


        row_to_append.append([next_run, step, "All", "AveragePositiveReward",  average_positive_reward/len(agents)])
        row_to_append.append([next_run, step, "All", "AverageNegativeReward",  average_negative_reward/len(agents)])


        row_to_append.append([next_run, step, "All", "Precission_X",  average_precission_X/len(agents)])
        row_to_append.append([next_run, step, "All", "Precission_!X",average_precission_notX/len(agents)])
        row_to_append.append([next_run, step, "All", "Recall_X",average_recall_X/len(agents)])
        row_to_append.append([next_run,step, "All", "Recall_!X", average_recall_notX/len(agents)])

        percentage_of_agents_survive = len(creatures) / self.agents_amount
        row_to_append.append([next_run, step, "All", "PercentageSurvive",  percentage_of_agents_survive])

        with open(test_run_name + '-results.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter =";")
            writer.writerows([[next_run, "GameOver", str(len(creatures)), str(step)]])
            writer.writerows(row_to_append)
        csvFile.close()


def object2rgb(ID_self, ID_other):
    '''
        If an object of ID_self is in vision range of an object ID,other, what
        does it see?
    '''
    if ID_self is None or int(str(ID_other)[:1]) == ID_PLANT or ID_other == ID_ROCK or ID_other == ID_TREE_TRUNK:
        # A plant and a rock always looks the same
        return id2rgb[ID_other]
    elif ID_self == ID_other:
        # Of the same species
        return id2rgb[ID_ANIMAL]
    else:
        # Another species
        return id2rgb[ID_OTHER]

def get_intensity(prox, prop):
    ''' 
        Calculate Vision Intensity.

        Parameters
        ----------

        prox : float
            the relative distance to the object (should be in [0,1] where 1 is 
            touching!)
        prop : float
            the size ratio of the object to us (where = 1 if same size, 0.1 if we
            are 10 times bigger than the object, etc.)

        Note: prox should be normalized. 

        Returns an intensity in [0,1] depending on size proportion and 
        (inversely) on distance. 
    '''
    # Actually we ignore the size for now
    return prox
