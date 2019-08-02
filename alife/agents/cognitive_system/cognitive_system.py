from .long_term_memory import LongTermMemory
from .working_memory import *
from .decision_making_system import *
from .observation_to_proposition_system import *
from .belief_revision_system import *
from .action import Action
import logging

class Cognitive_System():

    def __init__(self, observation_to_proposition_system: str, belief_revision_system: str, working_memory_system: str, decision_making_system: str, belief_revision_system_args, decision_making_system_args, closed_world_assumption: str):
        logging.basicConfig(filename="log.txt",
                                    filemode='a',
                                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                    datefmt='%H:%M:%S',
                                    level=logging.INFO)
        logging.info("\r\n")
        

        closed_world_assumption = True if closed_world_assumption == "True" else False

        if observation_to_proposition_system == "MultiplePropositionSystem":
            self.observation_to_proposition_system = MultiplePropositionSystem()
        elif observation_to_proposition_system == "OccamsRazorMultiplePropositionSystem":
            self.observation_to_proposition_system = OccamsRazorMultiplePropositionSystem()
        elif observation_to_proposition_system == "SinglePropositionSystem":
            self.observation_to_proposition_system = SinglePropositionSystem()
        elif observation_to_proposition_system == "RandomSinglePropositionSystem":
            self.observation_to_proposition_system = RandomSinglePropositionSystem()
        else:
            print("Observation System not found")

        if belief_revision_system == "FormalBeliefRevision":
            self.belief_revision_system = FormalBeliefRevision(closed_world_assumption, belief_revision_system_args)
        elif belief_revision_system == "ProbabilityBeliefRevision":
            self.belief_revision_system = ProbabilityBeliefRevision(closed_world_assumption, belief_revision_system_args)
        elif belief_revision_system == "RandomSinglePropositionSystem":
            self.belief_revision_system = ConditionalBeliefRevision(closed_world_assumption, belief_revision_system_args)
        else:
            print("Belief Revision System not found")
        
        if working_memory_system == "WorkingMemoryWithEvidence":
            self.working_memory_system = WorkingMemoryWithEvidence()
        elif working_memory_system == "WorkingMemoryWithActivationSpreading":
            self.working_memory_system = WorkingMemoryWithActivationSpreading()
        else:
            print("Working Memory System not found")

        if decision_making_system == "HumanLikeDecisionMakingUnderUncertaintySystem":
            self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem(decision_making_system_args)
        elif decision_making_system == "QLearningDecisionMakingSystem":
            self.decision_making_system = QLearningDecisionMakingSystem()
        else:
            print("Decision Making System not found")

        self.long_term_memory = LongTermMemory()

        logging.info("Cognitive System initialized")

    def act(self, agent, color_proposition, propositions, reward):
        # Eat or Not Eat?
        if color_proposition:
            logging.info("Received act request for agent %s, with color_proposition %s, propositions %s and reward %s"  %
            (agent.id_num, color_proposition.name if color_proposition is not None else "None", ",".join([proposition.name for proposition in propositions]), reward.name))

            generated_propositions = self.observation_to_proposition_system.observation_to_proposition(color_proposition, propositions, reward)
            logging.info("Generated Sentences:\r\n %s" % ( ",\r\n".join([generated_proposition.__str__() for generated_proposition in generated_propositions])))

            if reward == Reward.none:
                logging.info("Belief Base: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in self.long_term_memory.stored_sentences])))
                available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory.stored_sentences)
                logging.info("Available Knowledge: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                action_chosen = self.decision_making_system.make_decision(generated_propositions, available_knowledge)
                logging.info("Decision: %s, was made for generated proposition: %s and available knowledge: %s " % 
                (action_chosen, ",\r\n".join([generated_proposition.__str__() for generated_proposition in generated_propositions]), 
                    ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                return action_chosen
            else:
                available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory.stored_sentences)
                logging.info("Available Knowledge: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                self.decision_making_system.update_policy(reward, generated_propositions, available_knowledge)
                logging.info("Updated Decision Making Policy")
                revised_knowledge = self.belief_revision_system.revise_belief_base(generated_propositions, self.long_term_memory)
                self.long_term_memory.update(revised_knowledge)
                logging.info("Revised Belief Base: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in self.long_term_memory.stored_sentences])))
                # TODO What to do here? Eat or Not eat again? Does an decision need to made?
                # action_chosen = self.decision_making_system.make_decision(generated_propositions, available_knowledge)
                logging.info("Belief was revised, Belief Base was updated, Decision Making Policy was updated")

                return None
        # Walk arround random, or better prefere places where you wasnt before and later use spatial knowlege to look for good plants
        else:
            return Action.random


