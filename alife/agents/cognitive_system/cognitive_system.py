from .long_term_memory import LongTermMemory
from .working_memory import WorkingMemory
from .decision_making_system import DecisionMakingSystem
from .observation_to_proposition_system import *
from .belief_revision_system import *

class Cognitive_System():

    def __init__(self, observation_to_proposition_system: str, belief_revision_system: str, closed_world_assumption: str):
        closed_world_assumption = True if closed_world_assumption == "True" else False
        print(closed_world_assumption)
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

        self.observation_to_proposition_system = self.observation_to_proposition_systems.get(observation_to_proposition_system)
        self.belief_revision_system = self.belief_revision_systems.get(belief_revision_system)
        self.belief_revision_system.set_closed_world_assumption(closed_world_assumption)
        self.decision_making_system = DecisionMakingSystem()
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemory()
        print("Cognitive System initialized")

    def act(self, propositions, reward):
        available_revised_knowledge = []
        if propositions and reward:
            generated_propositions = self.observation_to_proposition_system.observation_to_proposition(propositions[0], propositions[1], reward)
            available_revised_knowledge = self.working_memory.retrieve_knowledge(generated_propositions, self.long_term_memory.stored_sentences)
            for generated_proposition in generated_propositions:
                available_revised_knowledge = self.belief_revision_system.revise_belief_base(generated_proposition, available_revised_knowledge)
        else:
            self.available_revised_knowledge = self.working_memory.retrieve_knowledge(None, self.long_term_memory.stored_sentences)
        self.long_term_memory.update(available_revised_knowledge)
        self.decision_making_system.make_decision(available_revised_knowledge)

