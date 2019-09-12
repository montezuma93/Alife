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
import yaml
import csv
import collections
class Cognitive_System():

    def __init__(self, observation_to_proposition_system: str, belief_revision_system: str, working_memory_system: str, decision_making_system: str,
         has_mental_map, observation_to_proposition_system_args, belief_revision_system_args, working_memory_system_args, decision_making_system_args,
         communication_system_args, yml_file = 'conf.yml',test_run_name=None):
        conf_yml = 'conf.yml' if yml_file is None else yml_file

        self.log_file_name = None
        if test_run_name is None:
            with open(conf_yml) as file:
                config_file = yaml.load(file)
                log_file = config_file['log_file']
                self.log_file_name = log_file['name']
            file.close()
        else:
            self.log_file_name = test_run_name + ".csv"

        

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
            self.evidence_interpretation = EvidenceInterpretation.evidence
        elif belief_revision_system == "ProbabilityBeliefRevision":
            self.belief_revision_system = ProbabilityBeliefRevision(belief_revision_system_args)
            self.evidence_interpretation = EvidenceInterpretation.probability
        elif belief_revision_system == "ConditionalBeliefRevision":
            self.belief_revision_system = ConditionalBeliefRevision(belief_revision_system_args)
            self.evidence_interpretation = EvidenceInterpretation.ranking
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
            self.decision_making_system = QLearningDecisionMakingSystem(decision_making_system_args)
        else:
            print("Decision Making System not found")

        self.mental_map = None
        if has_mental_map == "True":
            self.mental_map = MentalMap()
        self.long_term_memory = LongTermMemory()
        self.communication_system = CommunicationSystem(self.belief_revision_system, communication_system_args)

        self.last_action_chosen = None
        self.last_color_variable = None
        self.last_propositions = None
        self.last_reward = None
        self.last_generated_propositions = None
        self.last_available_knowledge = None
        self.last_agent_communicated_with = None



    def act(self, agent, color_proposition, propositions, reward, world, pos, currentHealth):
        rows_to_add_to_logger = []
        action_chosen = None

        porposition_list = None
        color_variable = None
        # Eat or Not Eat?
        if color_proposition:

            porposition_list = [proposition.variable for proposition in propositions]
            color_variable = color_proposition.variable

            generated_propositions = self.last_generated_propositions
            if color_variable != self.last_color_variable or collections.Counter(porposition_list) != collections.Counter(self.last_propositions) or reward != self.last_reward:
                generated_propositions = self.observation_to_proposition_system.observation_to_proposition(color_proposition, propositions, reward)
                self.last_generated_propositions = generated_propositions

            rows_to_add_to_logger.append([str(agent.id_num), "Observation", "# ".join([generated_proposition.__str__() for generated_proposition in generated_propositions])])
            rows_to_add_to_logger.append([agent.id_num, "Current Health", currentHealth])
            
            if reward == Reward.none:
                available_knowledge = self.last_available_knowledge
                if color_variable != self.last_color_variable or collections.Counter(porposition_list) != collections.Counter(self.last_propositions) or reward != self.last_reward:
                    available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory)
                    self.last_available_knowledge = available_knowledge
                
                self.decision_making_system.update_policy(reward, generated_propositions, available_knowledge, currentHealth)
                
                action_chosen = self.decision_making_system.make_decision(generated_propositions, available_knowledge, currentHealth)
                
                if type(self.decision_making_system) is HumanLikeDecisionMakingUnderUncertaintySystem:
                    rows_to_add_to_logger.append([agent.id_num, "DecisionMakingSystem", self.decision_making_system.solution_table])
                elif type(self.decision_making_system) is QLearningDecisionMakingSystem:
                    rows_to_add_to_logger.append([agent.id_num, "DecisionMakingSystem", self.decision_making_system.q_table])
                
                rows_to_add_to_logger.append([agent.id_num, "Action Chosen", action_chosen])
            else:
                
                rows_to_add_to_logger.append([agent.id_num, "Reward", reward.name])
                if self.mental_map and reward == Reward.nontoxic:
                    self.mental_map.remember_good_place(pos)
                available_knowledge = self.last_available_knowledge

                if color_variable != self.last_color_variable or collections.Counter(porposition_list) != collections.Counter(self.last_propositions) or reward != self.last_reward:
                    available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory)
                    self.last_available_knowledge = available_knowledge

                self.decision_making_system.update_policy(reward, generated_propositions, available_knowledge, currentHealth)
                if color_variable != self.last_color_variable or collections.Counter(porposition_list) != collections.Counter(self.last_propositions) or reward != self.last_reward:
                    revised_knowledge = self.belief_revision_system.revise_belief_base(generated_propositions, self.long_term_memory.stored_sentences)
                    
                    self.long_term_memory.update(revised_knowledge)
                
                    rows_to_add_to_logger.append([agent.id_num, "Belief", "# ".join([sentence.__str__() for sentence in self.long_term_memory.stored_sentences])])
                    # TODO What to do here? Eat or Not eat again? Does an decision need to made?
                    
                    available_knowledge = self.working_memory_system.retrieve_knowledge(generated_propositions, self.long_term_memory)
                    self.last_available_knowledge = available_knowledge

                action_chosen = self.decision_making_system.make_decision(generated_propositions, available_knowledge, currentHealth)
                
                if type(self.decision_making_system) is HumanLikeDecisionMakingUnderUncertaintySystem:
                    rows_to_add_to_logger.append([agent.id_num, "DecisionMakingSystem", self.decision_making_system.weightning_table])
                    rows_to_add_to_logger.append([agent.id_num, "DecisionMakingSystem", self.decision_making_system.solution_table])
                elif type(self.decision_making_system) is QLearningDecisionMakingSystem:
                    rows_to_add_to_logger.append([agent.id_num, "DecisionMakingSystem", self.decision_making_system.q_table])
                
                rows_to_add_to_logger.append([agent.id_num, "Action Chosen", action_chosen])
        # Walk arround random, or better prefere places where you wasnt before and later use spatial knowlege to look for good plants
        else:
            action_chosen = Action.explore
        
        # What to do now?
        # Move towards if eat
        # Explore if explore
        # Where to explore, depends on params as well as mental map
        if len(rows_to_add_to_logger) > 0:
            with open(self.log_file_name, 'a', newline='') as csvFile:
                writer = csv.writer(csvFile, delimiter =";")
                writer.writerows(rows_to_add_to_logger)
            csvFile.close()

        complete_action = None

        if self.mental_map is not None and action_chosen.name == Action.explore.name:
            if currentHealth.name == Health.moreThanHalf.name or  currentHealth.name == Health.moreThanThreeQuarter.name:
                complete_action = CompleteAction(action_chosen)

            elif currentHealth.name == Health.lessThanHalf.name or currentHealth.name == Health.lessThanQuarter.name:
                possible_locations = []
                for key, value in self.mental_map.mental_map.items():
                    if value == "X":
                        possible_locations.append(key)
                if len(possible_locations) == 0:
                    complete_action = CompleteAction(action_chosen)
                else:
                    best_location = None
                    smallest_distance = None
                    for location in possible_locations:
                        dist = math.sqrt((pos[0] - location[0])**2 + (pos[1] - location[1])**2)  
                        if smallest_distance is None or dist<smallest_distance:
                            smallest_distance = dist
                            best_location = (location[0],location[1])
                    complete_action = CompleteAction(action_chosen, best_location, self.mental_map)
        else:
            complete_action = CompleteAction(action_chosen)

        self.last_color_variable = color_variable
        self.last_propositions = porposition_list
        self.last_reward = reward
        return complete_action



    def communicate(self, agent, other_agent):
        if self.communication_system.able_to_communicate == 'True':
            if self.last_agent_communicated_with != other_agent:
                self.last_agent_communicated_with = other_agent
                rows_to_add_to_logger = []
                
                # Knowledge of the other agent
                other_agents_available_knowledge = other_agent.cognitive_system.working_memory_system.retrieve_knowledge(None, other_agent.cognitive_system.long_term_memory)
                rows_to_add_to_logger.append([agent.id_num, "Commnicate",  ",\r\n".join([sentence.__str__() for sentence in other_agents_available_knowledge])])
                new_information = self.communication_system.filter_sentences(other_agents_available_knowledge)
                revised_knowledge = self.belief_revision_system.revise_belief_base(new_information, self.long_term_memory.stored_sentences)
                self.long_term_memory.update(revised_knowledge)

                if len(rows_to_add_to_logger) > 0:
                    with open(self.log_file_name, 'a') as csvFile:
                        writer = csv.writer(csvFile, delimiter =";")
                        writer.writerows(rows_to_add_to_logger)
                    csvFile.close()
                