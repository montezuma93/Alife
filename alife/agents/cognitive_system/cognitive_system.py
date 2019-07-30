from .long_term_memory import LongTermMemory
from .working_memory import WorkingMemory
from .decision_making_system import DecisionMakingSystem
from .observation_to_proposition_system import *
from .belief_revision_system import *
import logging

class Cognitive_System():

    def __init__(self, observation_to_proposition_system: str, belief_revision_system: str, belief_revision_system_args, closed_world_assumption: str):

        logging.basicConfig(filename="log.txt",
                                    filemode='a',
                                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                    datefmt='%H:%M:%S',
                                    level=logging.INFO)
        logging.info("\r\n")
        

        closed_world_assumption = True if closed_world_assumption == "True" else False
        self.observation_to_proposition_systems = {
            "MultiplePropositionSystem": MultiplePropositionSystem(),
            "OccamsRazorMultiplePropositionSystem": OccamsRazorMultiplePropositionSystem(),
            "SinglePropositionSystem": SinglePropositionSystem(),
            "RandomSinglePropositionSystem": RandomSinglePropositionSystem()
        }
        self.belief_revision_systems = {
            "FormalBeliefRevision": FormalBeliefRevision(closed_world_assumption, belief_revision_system_args),
            "ProbabilityBeliefRevision": ProbabilityBeliefRevision(closed_world_assumption, belief_revision_system_args),
            "ConditionalBeliefRevision": ConditionalBeliefRevision(closed_world_assumption, belief_revision_system_args)
        }

        self.observation_to_proposition_system = self.observation_to_proposition_systems.get(observation_to_proposition_system)
        self.belief_revision_system = self.belief_revision_systems.get(belief_revision_system)
        self.decision_making_system = DecisionMakingSystem()
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemory()
        logging.info("Cognitive System initialized")

    def act(self, propositions, reward):
        available_revised_knowledge = []
        if propositions and reward:
            logging.info("Received act request with new observation")
            generated_propositions = self.observation_to_proposition_system.observation_to_proposition(propositions[0], propositions[1], reward)
            available_revised_knowledge = self.working_memory.retrieve_knowledge(generated_propositions, self.long_term_memory.stored_sentences)
            for generated_proposition in generated_propositions:
                available_revised_knowledge = self.belief_revision_system.revise_belief_base(generated_proposition, available_revised_knowledge)
        else:
            self.available_revised_knowledge = self.working_memory.retrieve_knowledge(None, self.long_term_memory.stored_sentences)
        self.long_term_memory.update(available_revised_knowledge)
        self.decision_making_system.make_decision(available_revised_knowledge)

