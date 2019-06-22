from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import OberservationToPropositionSystem

class Cognitive_System():

    def __init__(self):
        self.long_term_memory = LongTermMemory()
        self.observation_to_proposition_system = OberservationToPropositionSystem(True)
        print("initialized")

