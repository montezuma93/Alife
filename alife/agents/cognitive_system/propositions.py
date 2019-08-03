from enum import Enum

# Sentence([([proposition, proposition, ...], reward), ([proposition, proposition, ...], reward), ...], evidence)
class Sentence():
    def __init__(self, propositions: list, evidence: float):
        # Tuple
        self.propositions = propositions
        self.evidence = evidence

    def __str__(self):
        or_sentences = []
        for sentence in self.propositions:
            proposition_ands = "^".join([proposition.name for proposition in sentence[0]])
            reward = sentence[1]
            or_sentences.append("propositions: {0}, reward: {1} ".format(proposition_ands, reward))
        
        
        return "Sentence: {0}, evidence: {1} ".format(" v ".join(or_sentences), self.evidence)

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

def get_variable_names_for_color_propositions():
    return ["G", "O", "B", "P"]

def get_variable_names_for_reward_propositions():
    return ["X"]

def get_variable_names_for_all_propositions():
    return get_variable_names_for_color_propositions() + get_variable_names_for_propositions() + get_variable_names_for_reward_propositions()
    
class Reward(Enum):
    toxic= "X"
    nontoxic= "!X"
    none="~"
