import numpy
import math
class MentalMap:

    def __init__(self):
        self.mental_map = {}

    def remember_good_place(self, pos):
        pos_x = int(pos[0])
        pos_y = int(pos[1])
        already_in_map = False
        for entry, value in self.mental_map.items():
            dist = math.sqrt((pos_x - entry[0])**2 + (pos_y - entry[1])**2)
            if dist < 25:
                already_in_map = True
        if not already_in_map:
            self.mental_map[(pos_x,pos_y)] = "X"

    def remove(self, pos):
        del self.mental_map[(pos[0], pos[1])]



    
