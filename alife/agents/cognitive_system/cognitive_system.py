from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import *

class Cognitive_System():

    def __init__(self, observation_to_proposition_system: str):
        self.observation_to_proposition_systems = {
            "MultiplePropositionSystem": MultiplePropositionSystem(),
            "OccamsRazorMultiplePropositionSystem": OccamsRazorMultiplePropositionSystem(),
            "SinglePropositionSystem": SinglePropositionSystem(),
            "RandomSinglePropositionSystem": RandomSinglePropositionSystem()
        }
        self.long_term_memory = LongTermMemory()
        self.observation_to_proposition_system = self.observation_to_proposition_systems.get(observation_to_proposition_system)
        print("Cognitive System initialized")
