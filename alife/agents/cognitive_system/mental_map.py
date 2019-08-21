import numpy
class MentalMap:

    def __init__(self):
        self.mental_map = {}

    def remember_good_place(self, pos):
        self.mental_map[pos] = "X"
    
    def remember_place(self, pos):
        self.mental_map[pos] = "O"
    
