from enum import Enum

class Proposition():
    def __init__(self):
        pass

class NextToProposition(Proposition):
    def __init__(self):
        pass

class NextToRock(NextToProposition):
    def __init__(self):
        pass

class NextToTreeTrunk(NextToProposition):
    def __init__(self):
        pass


class TimeProposition(Proposition):
    def __init__(self):
        pass

class DayProposition(TimeProposition):
    def __init__(self):
        pass

class NightProposition(TimeProposition):
    def __init__(self):
        pass


class ColorProposition(Proposition):
    def __init__(self):
        pass

class ColorGreen(ColorProposition):
    def __init__(self):
        pass

class ColorOrange(ColorProposition):
    def __init__(self):
        pass

class ColorPurple(ColorProposition):
    def __init__(self):
        pass

class ColorTurquoise(ColorProposition):
    def __init__(self):
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