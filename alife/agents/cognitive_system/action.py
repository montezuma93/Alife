from enum import Enum

class Action(Enum):
    move_towards = "EAT"
    move_elsewhere= "!EAT"
    random="~"
