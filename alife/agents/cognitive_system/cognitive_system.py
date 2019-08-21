from .long_term_memory import LongTermMemory
from .communication_system import CommunicationSystem
from .working_memory import *
from .decision_making_system import *
from .observation_to_proposition_system import *
from .propositions import *
from .belief_revision_system import *
from .action import Action
from .mental_map import MentalMap
import logging

class Cognitive_System():

    def __init__(self, observation_to_proposition_system: str, belief_revision_system: str, working_memory_system: str, decision_making_system: str,
         has_mental_map, observation_to_proposition_system_args, belief_revision_system_args, working_memory_system_args, decision_making_system_args):


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

        self.mental_map = None
        if has_mental_map == "True":
            self.mental_map = MentalMap()
        self.long_term_memory = LongTermMemory()
        self.communication_system = CommunicationSystem(self.belief_revision_system)

        logging.info("Cognitive System initialized")

    def act(self, agent, color_proposition, propositions, reward, world, pos, currentHealth):
        position = world.pos2grid(pos)
        action_chosen = None
        if self.mental_map:
            self.mental_map.remember_place(position)
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
                logging.info("Decision: %s, was made for generated proposition: %s and available knowledge: %s" % 
                (action_chosen, ",\r\n".join([generated_proposition.__str__() for generated_proposition in generated_propositions]), 
                    ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
            else:
                if self.mental_map and reward == Reward.nontoxic:
                    self.mental_map.remember_good_place(pos)
                available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory)
                logging.info("Available Knowledge: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                self.decision_making_system.update_policy(reward, generated_propositions, available_knowledge)
                logging.info("Updated Decision Making Policy")
                if type(self.decision_making_system) is QLearningDecisionMakingSystem:
                    logging.info("Q Table: \r\n %s" % (self.decision_making_system.q_table))
                logging.info("Sentences to revise belief base: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in generated_propositions])))
                revised_knowledge = self.communication_system.communicate(self.long_term_memory.stored_sentences, generated_propositions)
                self.long_term_memory.update(revised_knowledge)
                logging.info("Revised Belief Base: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in self.long_term_memory.stored_sentences])))
                logging.info("Belief was revised, Belief Base was updated, Decision Making Policy was updated")
                # TODO What to do here? Eat or Not eat again? Does an decision need to made?
                available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory)
                logging.info("Available Knowledge: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
                action_chosen = self.decision_making_system.make_decision(generated_propositions, available_knowledge)
                logging.info("Decision: %s, was made for generated proposition: %s and available knowledge: %s:" % 
                (action_chosen, ",\r\n".join([generated_proposition.__str__() for generated_proposition in generated_propositions]), 
                    ",\r\n".join([sentence.__str__() for sentence in available_knowledge])))
        # Walk arround random, or better prefere places where you wasnt before and later use spatial knowlege to look for good plants
        else:
            action_chosen = Action.explore
        # What to do now?
        # Move towards if eat
        # Explore if explore
        # Where to explore, depends on params as well as mental map
        
        complete_action = None

        if self.mental_map is not None and action_chosen.name == Action.explore.name:
            logging.info("Mental Map is availaible: %s, with current health: %s, looking for best spot" % (self.mental_map.mental_map, currentHealth.value))
            x,y = world.pos2grid(pos)
            if currentHealth.name == Health.moreThanHalf.name:
                possible_locations = []
                for i in [x-1,x, x+1]:
                    for j in [y-1,y, y+1]:
                        if (i,j) not in self.mental_map.mental_map.keys():
                            possible_locations.append((i,j))
                if len(possible_locations) == 0:
                    complete_action = CompleteAction(action_chosen)
                else:
                    best_location = None
                    smallest_distance = None
                    for location in possible_locations:
                        grid_pos = world.grid2pos((location[0],location[1]))
                        dist = math.sqrt((x - grid_pos[0])**2 + (y - grid_pos[1])**2)  
                        if smallest_distance is None or dist<smallest_distance:
                            smallest_distance = dist
                            best_location = (i,j)
                    complete_action = CompleteAction(action_chosen, best_location)

            elif currentHealth.name == Health.lessThanHalf.name or currentHealth.name == Health.lessThanQuarter.name:
                possible_locations = []
                for key, value in self.mental_map.mental_map.items():
                    if value == "X":
                        possible_locations.append(key)
                if len(possible_locations) == 0:
                    for i in [x-1,x, x+1]:
                        for j in [y-1,y, y+1]:
                            if (i,j) not in self.mental_map.mental_map.keys():
                                possible_locations.append((i,j))
                if len(possible_locations) == 0:
                    complete_action = CompleteAction(action_chosen)
                else:
                    best_location = None
                    smallest_distance = None
                    for location in possible_locations:
                        grid_pos = world.grid2pos((location[0],location[1]))
                        dist = math.sqrt((x - grid_pos[0])**2 + (y - grid_pos[1])**2)  
                        if smallest_distance is None or dist<smallest_distance:
                            smallest_distance = dist
                            best_location = (i,j)
                    complete_action = CompleteAction(action_chosen, best_location)
        else:
            complete_action = CompleteAction(action_chosen)

        return complete_action



    def communicate(self, agent, other_agent):
        logging.info("Received communication request for agent %s from agent %s" % (agent.id_num, other_agent.id_num))
        # Knowledge of the other agent
        other_agents_available_knowledge = other_agent.cognitive_system.working_memory_system.retrieve_knowledge(None, other_agent.cognitive_system.long_term_memory)
        logging.info("Available Knowledge of the other agent: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in other_agents_available_knowledge])))
        new_information = self.communication_system.filter_sentences(other_agents_available_knowledge)
        logging.info("Information, used from the other agent: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in new_information])))
        revised_knowledge = self.belief_revision_system.revise_belief_base(new_information, self.long_term_memory.stored_sentences)
        self.long_term_memory.update(revised_knowledge)
        logging.info("Revised Belief Base: \r\n %s" % ( ",\r\n".join([sentence.__str__() for sentence in self.long_term_memory.stored_sentences])))