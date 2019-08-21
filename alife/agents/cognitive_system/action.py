from enum import Enum

class CompleteAction:

    def __init__(self, intension, location=None):
        self.intension = intension 
        self.location = location

class Action(Enum):
    eat = "EAT"
    explore= "EXPLORE"