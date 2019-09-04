from enum import Enum
import math

class CompleteAction:

    def __init__(self, intension, location=None, mental_map = None):
        self.intension = intension 
        self.location = location
        self.mental_map = mental_map

class Action(Enum):
    eat = "EAT"
    explore= "EXPLORE"