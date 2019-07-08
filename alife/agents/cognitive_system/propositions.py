from enum import Enum

# Sentence([([color_proposition], reward)], evidence)
class Sentence():
    def __init__(self, propositions: list, evidence: float):
        # Tuple
        self.propositions = propositions
        self.evidence = evidence

class Proposition():
    def __init__(self):
        pass

class NextToProposition(Proposition):
    def __init__(self):
        pass

class NextToRock(NextToProposition):
    variable = "R"
    def __init__(self):
        self.variable = "R"
        self.name = "ROCK"
        pass

class NextToTreeTrunk(NextToProposition):
    variable = "T"
    def __init__(self):
        self.variable = "T"
        self.name = "TREE"
        pass


class TimeProposition(Proposition):
    def __init__(self):
        pass

class DayProposition(TimeProposition):
    variable = "D"
    def __init__(self):
        self.variable = "D"
        self.name = "DAY"
        pass

class NightProposition(TimeProposition):
    variable = "!D"
    def __init__(self):
        self.variable = "!D"
        self.name = "!DAY"
        pass

class ColorProposition(Proposition):
    def __init__(self):
        pass

class ColorGreen(ColorProposition):
    variable = "G"
    def __init__(self):
        self.variable = "G"
        self.name = "GREEN"
        pass

class ColorOrange(ColorProposition):
    variable = "O"
    def __init__(self):
        self.variable = "O"
        self.name = "ORANGE"
        pass

class ColorPurple(ColorProposition):
    variable = "P"
    def __init__(self):
        self.variable = "P"
        self.name = "PURPLE"
        pass

class ColorBlue(ColorProposition):
    variable = "B"
    def __init__(self):
        self.variable = "B"
        self.name = "BLUE"
        pass

class SpatialProposition(Proposition):
    def __init__(self):
        pass

class NorthOfProposition(SpatialProposition):
    def __init__(self, agent, referent):
        self.agent = referent
        self.agent = referent

class SouthOfProposition(SpatialProposition):
    def __init__(self, agent, referent):
        self.agent = referent
        self.agent = referent

class WestOfProposition(SpatialProposition):
    def __init__(self, agent, referent):
        self.agent = referent
        self.agent = referent

class EastOfProposition(SpatialProposition):
    def __init__(self, agent, referent):
        self.agent = referent
        self.agent = referent

def get_variable_names_for_propositions():
    return ["R", "T", "D"]

class Reward(Enum):
    toxic= "X"
    nontoxic= "!X"