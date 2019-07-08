from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import *
from .belief_revision_system import *

class Cognitive_System():

    def __init__(self, observation_to_proposition_system: str, belief_revision_system: str):
        self.observation_to_proposition_systems = {
            "MultiplePropositionSystem": MultiplePropositionSystem(),
            "OccamsRazorMultiplePropositionSystem": OccamsRazorMultiplePropositionSystem(),
            "SinglePropositionSystem": SinglePropositionSystem(),
            "RandomSinglePropositionSystem": RandomSinglePropositionSystem()
        }
        self.belief_revision_systems = {
            "FormalBeliefRevision": FormalBeliefRevision(),
            "ProbabilityBeliefRevision": ProbabilityBeliefRevision(),
            "ConditionalBeliefRevision": ConditionalBeliefRevision()
        }
        self.long_term_memory = LongTermMemory()
        self.observation_to_proposition_system = self.observation_to_proposition_systems.get(observation_to_proposition_system)
        self.belief_revision_system = self.belief_revision_systems.get(belief_revision_system)
        print(self.belief_revision_system.closed_world_assumption)
        print("Cognitive System initialized")
