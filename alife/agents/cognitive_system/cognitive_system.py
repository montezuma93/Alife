from .long_term_memory import LongTermMemory
from .communication_system import CommunicationSystem
from .working_memory import *
from .decision_making_system import *
from .observation_to_proposition_system import *
from .belief_revision_system import *
from .action import Action
import logging

class Cognitive_System():

    def __init__(self, observation_to_proposition_system: str, belief_revision_system: str, working_memory_system: str, decision_making_system: str,
         observation_to_proposition_system_args, belief_revision_system_args, working_memory_system_args, decision_making_system_args):


        self.factor_for_communication_sentenes = 0.5

        logging.basicConfig(filename="log.txt",
                                    filemode='a',
                                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                    datefmt='%H:%M:%S',
                                    level=logging.INFO)
        logging.info("\r\n")

        if observation_to_proposition_system == "MultiplePropositionSystem":
            self.observation_to_proposition_system = MultiplePropositionSystem(observation_to_proposition_system_args)
        elif observation_to_proposition_system == "OccamsRazorMultiplePropositionSystem":
            self.observation_to_proposition_system = OccamsRazorMultiplePropositionSystem(observation_to_proposition_system_args)
        elif observation_to_proposition_system == "SinglePropositionSystem":
            self.observation_to_proposition_system = SinglePropositionSystem(observation_to_proposition_system_args)
        elif observation_to_proposition_system == "RandomSinglePropositionSystem":
            self.observation_to_proposition_system = RandomSinglePropositionSystem(observation_to_proposition_system_args)
        else:
            print("Observation System not found")

        if belief_revision_system == "FormalBeliefRevision":
            self.belief_revision_system = FormalBeliefRevision(belief_revision_system_args)
        elif belief_revision_system == "ProbabilityBeliefRevision":
            self.belief_revision_system = ProbabilityBeliefRevision(belief_revision_system_args)
        elif belief_revision_system == "RandomSinglePropositionSystem":
            self.belief_revision_system = ConditionalBeliefRevision(belief_revision_system_args)
        else:
            print("Belief Revision System not found")
        
        if working_memory_system == "WorkingMemoryWithEvidence":
            self.working_memory_system = WorkingMemoryWithEvidence(working_memory_system_args)
        elif working_memory_system == "WorkingMemoryWithActivationSpreading":
            self.working_memory_system = WorkingMemoryWithActivationSpreading(working_memory_system_args)
        else:
            print("Working Memory System not found")

        if decision_making_system == "HumanLikeDecisionMakingUnderUncertaintySystem":
            self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem(decision_making_system_args)
        elif decision_making_system == "QLearningDecisionMakingSystem":
            self.decision_making_system = QLearningDecisionMakingSystem()
        else:
            print("Decision Making System not found")

        self.long_term_memory = LongTermMemory()
        self.communication_system = CommunicationSystem()

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
                available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory)
                logging.info("Available Knowledge: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                action_chosen = self.decision_making_system.make_decision(generated_propositions, available_knowledge)
                logging.info("Decision: %s, was made for generated proposition: %s and available knowledge: %s " % 
                (action_chosen, ",\r\n".join([generated_proposition.__str__() for generated_proposition in generated_propositions]), 
                    ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                return action_chosen
            else:
                available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory)
                logging.info("Available Knowledge: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                self.decision_making_system.update_policy(reward, generated_propositions, available_knowledge)
                logging.info("Updated Decision Making Policy")
                if type(self.decision_making_system) is QLearningDecisionMakingSystem:
                    logging.info("Q Table: \r\n %s" % (self.decision_making_system.q_table))
                revised_knowledge = self.belief_revision_system.revise_belief_base(generated_propositions, self.long_term_memory.stored_sentences)
                self.long_term_memory.update(revised_knowledge)
                logging.info("Revised Belief Base: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in self.long_term_memory.stored_sentences])))

                logging.info("Belief was revised, Belief Base was updated, Decision Making Policy was updated")

                # TODO What to do here? Eat or Not eat again? Does an decision need to made?
                available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory)
                logging.info("Available Knowledge: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                action_chosen = self.decision_making_system.make_decision(generated_propositions, available_knowledge)
                logging.info("Decision: %s, was made for generated proposition: %s and available knowledge: %s " % 
                (action_chosen, ",\r\n".join([generated_proposition.__str__() for generated_proposition in generated_propositions]), 
                    ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))

                return action_chosen
        # Walk arround random, or better prefere places where you wasnt before and later use spatial knowlege to look for good plants
        else:
            choice = random.choices(population=[Action.move_towards, Action.move_elsewhere], weights=[0.8, 0.2], k=1)
            return choice[0]

    def communicate(self, agent, other_agent):
        logging.info("Received communication request for agent %s from agent %s" % (agent.id_num, other_agent.id_num))
        # Knowledge of the other agent
        other_agents_available_knowledge = other_agent.cognitive_system.working_memory_system.retrieve_knowledge(None, other_agent.cognitive_system.long_term_memory)
        logging.info("Available Knowledge of the other agent: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in other_agents_available_knowledge])))
        new_information = self.communication_system.communicate(other_agents_available_knowledge)
        logging.info("Information, used from the other agent: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in new_information])))
        revised_knowledge = self.belief_revision_system.revise_belief_base(new_information, self.long_term_memory.stored_sentences)
        self.long_term_memory.update(revised_knowledge)
        logging.info("Revised Belief Base: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in self.long_term_memory.stored_sentences])))