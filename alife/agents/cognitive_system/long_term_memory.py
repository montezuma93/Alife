from .propositions import *

class LongTermMemory:

    def __init__(self):
        self.stored_proposition = {}
        for cls in Proposition.__subclasses__():
            self.stored_proposition[cls.__name__] = []

    def save_proposition(self, proposition_to_save: Proposition):
        for base in proposition_to_save.__class__.__bases__:
            self.stored_proposition[base.__name__].append(proposition_to_save)
