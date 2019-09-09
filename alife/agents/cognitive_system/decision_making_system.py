from .propositions import *
from .action import Action, CompleteAction
from .long_term_memory import LongTermMemory
import copy
import math
import operator
import itertools
from .truths.truthtable import *
import random
import collections
# See: Towards agents with human-like decisions under uncertainty
class HumanLikeDecisionMakingUnderUncertaintySystem:

    def __init__(self, decision_making_system_args):
        self.risk_aversion = int(decision_making_system_args[0])
        self.ambiguity_aversion = int(decision_making_system_args[1])
        self.evidence_interpretation = decision_making_system_args[2]
        self.closed_world_assumption = decision_making_system_args[3]
        self.last_observations = None
        self.last_available_sentences = None
        self.use_recent_health = decision_making_system_args[4] 

        self.epsilon = 0.1
        self.delta = 0.77
        self.gamma = 0.44
        self.alpha = 0.88
        self.k = 0.2

        if self.use_recent_health:
            self.utility_table = {
                "eat->75":int(decision_making_system_args[5]),
                "eat->=50":int(decision_making_system_args[6]),
                "eat-<50":int(decision_making_system_args[7]),
                "eat-<25":int(decision_making_system_args[8]),
                "explore->75":int(decision_making_system_args[9]),
                "explore->=50":int(decision_making_system_args[10]),
                "explore-<50":int(decision_making_system_args[11]),
                "explore-<25":int(decision_making_system_args[12])
            }
        else:
            self.utility_table = {
                "eat":int(decision_making_system_args[5]),
                "explore":int(decision_making_system_args[6])
            }

        self.weightning_table = {
            "eat":{
                "true":0,
                "false":0,
            }
        }
        self.solution_table = {
            "eat":0, # eat
            "explore":0 # walking
        }
        self.solution_to_action_mapping = {
            "eat": Action.eat,
            "explore": Action.explore
        }

    # Observation = [Proposition,...], [...]
    def make_decision(self, observations, available_sentences, recent_health):

        if collections.Counter(observations) != collections.Counter(self.last_observations) or collections.Counter(available_sentences) != collections.Counter(self.last_available_sentences):
            # Utility eat = Eat Non Toxic - Eat toxic , needs to be greater 1 by design
           
            if self.evidence_interpretation == EvidenceInterpretation.evidence.value:
                self.adjust_weightning_table_for_evidence(observations, available_sentences)
                for key, value in self.weightning_table.items():
                    total_evidence = self.weightning_table[key]["true"] +self.weightning_table[key]["false"]
                    for key2, value2 in value.items():
                        self.weightning_table[key][key2] = self.weightning_table[key][key2] / total_evidence
            elif self.evidence_interpretation == EvidenceInterpretation.probability.value:
                self.adjust_weightning_table_for_probability(observations, available_sentences)
                for key, value in self.weightning_table.items():
                    total_evidence = self.weightning_table[key]["true"] +self.weightning_table[key]["false"]
                    for key2, value2 in value.items():
                        self.weightning_table[key][key2] = self.weightning_table[key][key2] / total_evidence
            elif self.evidence_interpretation == EvidenceInterpretation.ranking.value:
                self.adjust_weightning_table_for_ranking(observations, available_sentences)
                for key, value in self.weightning_table.items():
                    total_evidence = self.weightning_table[key]["true"] +self.weightning_table[key]["false"]
                    for key2, value2 in value.items(): 
                        self.weightning_table[key][key2] = self.weightning_table[key][key2] / total_evidence
        # Calculate entropy
        for key, value in self.weightning_table.items():
            if self.weightning_table[key]["true"] == 0 or self.weightning_table[key]["false"] == 0:
                self.weightning_table[key]["entropy"] = 0
            else:
                self.weightning_table[key]["entropy"] = (self.weightning_table[key]["true"] * math.log(self.weightning_table[key]["true"]) + self.weightning_table[key]["false"] * math.log(self.weightning_table[key]["false"])) * -1

        for key in self.solution_table.keys():
            utility = 0
            if self.use_recent_health:
                utility = math.pow(self.utility_table[key + "-" + recent_health.value], self.alpha)
            else:
                utility = math.pow(self.utility_table[key], self.alpha)
            ambiguity_of_solution = self.weightning_table[key]["entropy"] if key in self.weightning_table else 0
            
            normalized_ambiguity_of_solution = (1 - math.pow(math.e, (self.k * ambiguity_of_solution * -1)))
            probability = self.weightning_table[key]["true"] if key in self.weightning_table else 1
            counter_probability = self.weightning_table[key]["false"] if key in self.weightning_table else 0
            weightning = ((self.delta + 0.5 - self.risk_aversion) * (1-self.ambiguity_aversion * normalized_ambiguity_of_solution) * math.pow(probability,self.gamma)) / (
                ((self.delta + 0.5 - self.risk_aversion) * (1-self.ambiguity_aversion * normalized_ambiguity_of_solution) * math.pow(probability,self.gamma)) +  math.pow(counter_probability,self.gamma))
            self.solution_table[key] = utility * weightning

        decision_made = self.solution_to_action_mapping.get(max(self.solution_table.items(), key=operator.itemgetter(1))[0])
        self.last_observations = observations
        self.last_available_sentences = available_sentences
        return decision_made

    def adjust_weightning_table_for_evidence(self, observations, available_sentences):
        evidence_for_non_toxic= 0
        evidence_for_toxic= 0
        
        for observation in observations:
            non_toxic_observation = self.create_truth_table_for_new_sentence(observation, "!X")
            toxic_observation = self.create_truth_table_for_new_sentence(observation, "X")
            evidence_for_non_toxic = evidence_for_non_toxic + self.calculate_b_m_rank(non_toxic_observation, available_sentences)
            evidence_for_toxic = evidence_for_toxic + self.calculate_b_m_rank(toxic_observation, available_sentences)
        self.weightning_table["eat"]["true"] = evidence_for_non_toxic if evidence_for_non_toxic > 0 else self.epsilon
        self.weightning_table["eat"]["false"] = evidence_for_toxic if evidence_for_toxic > 0 else self.epsilon


    def adjust_weightning_table_for_ranking(self, observations, available_sentences):
        evidence_for_non_toxic= 0
        evidence_for_toxic= 0
        for observation in observations:
            if self.closed_world_assumption:
                if not any([isinstance(observation_proposition, type(NightProposition())) for observation_proposition in observation.propositions[0][0]]) and not any([isinstance(observation_proposition, type(DayProposition())) for observation_proposition in observation.propositions[0][0]]):
                    observation.propositions[0][0].append(NightProposition())
            sentence_of_observation = None
            for sentence in available_sentences:
                if (all(any(isinstance(sentence_proposition, type(observation_proposition)) for sentence_proposition in sentence.propositions[0][0]) for observation_proposition in observation.propositions[0][0])
                 and all(any(isinstance(observation_proposition, type(sentence_proposition)) for observation_proposition in observation.propositions[0][0]) for sentence_proposition in sentence.propositions[0][0]) 
                 and sentence.propositions[0][1] == Reward.nontoxic):
                    sentence_of_observation = sentence
            evidence_for_non_toxic = evidence_for_non_toxic + 1/max(sentence_of_observation.evidence, self.epsilon) if sentence_of_observation is not None else evidence_for_non_toxic
            sentence_of_observation = None
            for sentence in available_sentences:
                if (all(any(isinstance(sentence_proposition, type(observation_proposition)) for sentence_proposition in sentence.propositions[0][0]) for observation_proposition in observation.propositions[0][0]) 
                 and all(any(isinstance(observation_proposition, type(sentence_proposition)) for observation_proposition in observation.propositions[0][0]) for sentence_proposition in sentence.propositions[0][0])
                 and sentence.propositions[0][1] == Reward.toxic):
                    sentence_of_observation = sentence
            evidence_for_toxic = evidence_for_toxic + 1/max(sentence_of_observation.evidence,self.epsilon) if sentence_of_observation is not None else evidence_for_toxic
        self.weightning_table["eat"]["true"] = evidence_for_non_toxic if evidence_for_non_toxic > 0 else self.epsilon
        self.weightning_table["eat"]["false"] = evidence_for_toxic if evidence_for_toxic > 0 else self.epsilon

    def adjust_weightning_table_for_probability(self, observations, available_sentences):
        evidence_for_non_toxic= 0
        evidence_for_toxic= 0
        for observation in observations:
            observation_to_use = observation
            if self.closed_world_assumption:
                if not any([isinstance(observation_proposition, type(NightProposition())) for observation_proposition in observation_to_use.propositions[0][0]]) and not any([isinstance(observation_proposition, type(DayProposition())) for observation_proposition in observation_to_use.propositions[0][0]]):
                    observation_to_use = copy.deepcopy(observation)
                    observation_to_use.propositions[0][0].append(NightProposition())
            sentence_of_observation = None
            for sentence in available_sentences:
                if (all(any(isinstance(sentence_proposition, type(observation_proposition)) for sentence_proposition in sentence.propositions[0][0]) for observation_proposition in observation_to_use.propositions[0][0])
                 and all(any(isinstance(observation_proposition, type(sentence_proposition)) for observation_proposition in observation_to_use.propositions[0][0]) for sentence_proposition in sentence.propositions[0][0]) 
                 and sentence.propositions[0][1] == Reward.nontoxic):
                    sentence_of_observation = sentence
            evidence_for_non_toxic = evidence_for_non_toxic + sentence_of_observation.evidence if sentence_of_observation is not None else evidence_for_non_toxic
            sentence_of_observation = None
            for sentence in available_sentences:
                if (all(any(isinstance(sentence_proposition, type(observation_proposition)) for sentence_proposition in sentence.propositions[0][0]) for observation_proposition in observation_to_use.propositions[0][0]) 
                 and all(any(isinstance(observation_proposition, type(sentence_proposition)) for observation_proposition in observation_to_use.propositions[0][0]) for sentence_proposition in sentence.propositions[0][0])
                 and sentence.propositions[0][1] == Reward.toxic):
                    sentence_of_observation = sentence
            evidence_for_toxic = evidence_for_toxic + sentence_of_observation.evidence if sentence_of_observation is not None else evidence_for_toxic
        self.weightning_table["eat"]["true"]= evidence_for_non_toxic if evidence_for_non_toxic > 0 else self.epsilon
        self.weightning_table["eat"]["false"]= evidence_for_toxic if evidence_for_toxic > 0 else self.epsilon

    def calculate_b_m_rank(self, sentence_truth_table, belief_base):
        belief_base_sentences = sorted(belief_base, key=lambda x: x.evidence, reverse=False)

        next_index_to_check = len(belief_base_sentences)-1
        while next_index_to_check >= 0:
            evidence = belief_base_sentences[next_index_to_check].evidence
            belief_base_sentences_with_at_least_evidence = []
            for index, sentence in reversed(list(enumerate(belief_base_sentences))):
                if sentence.evidence >= evidence:
                    belief_base_sentences_with_at_least_evidence.append(sentence)
                    next_index_to_check = index - 1

            # Check B entails varphi
            belief_base_truth_table_with_at_least_evidence = self.create_truth_table_for_belief_base(belief_base_sentences_with_at_least_evidence)
            if self.belief_base_infers_sentence(belief_base_truth_table_with_at_least_evidence, sentence_truth_table):
                return evidence
        return 0

    def create_truth_table_for_belief_base(self, belief_base: list):
            # All sentences, will be combined later with "AND"
        sentences = []
        # All sentences in a belief base
        for and_sentence in belief_base:
            # "OR" propositions, no logic yet for that part
            or_parts = []
            for sentence in and_sentence.propositions:
                # All variables found in the conjuction parts of the sentence, is need to be able to add non available variables, if closed world assumption is active
                available_variables = []
                for proposition in sentence[0]:
                    available_variables.append(proposition.variable)
                # If closed world assumption is set to true, for not available fact, it will be assumed that the negation holds
                # i.e if D is not in the setence, !D is assumed
                # Otherwise (D v !D) is assumed, but (D v !D) is always true and can be ignored
                if self.closed_world_assumption:
                    all_proposition_variable_names = get_variable_names_for_propositions()
                    for proposition in all_proposition_variable_names:
                        if not available_variables.__contains__(proposition) and not available_variables.__contains__("!" + proposition):
                            available_variables.append("!"+proposition )
                # Combine variables by conjunction
                conjuction_part =available_variables[0].replace("!", "") if "!" in available_variables[0] else "!"+ available_variables[0]
                i = 1
                while i < len(available_variables):
                    conjuction_part = "(" + conjuction_part  + "|" + available_variables[i].replace("!", "") + ")" if "!" in available_variables[i] else "(" + conjuction_part  + "|" + "!"+ available_variables[i] + ")"
                    i += 1
                or_parts.append("((" + conjuction_part + ")" + "|" + sentence[1].value + ")")
            # Adding up all or parts
            complete_sentence_or_sentence = or_parts[0]
            i = 1
            while i < len(or_parts):
                complete_sentence_or_sentence = "(" + complete_sentence_or_sentence  + "|" + or_parts[i] + ")"
                i += 1
            sentences.append(complete_sentence_or_sentence)
        # Adding up all parts
        complete_sentence = sentences[0]
        i = 1
        while i < len(sentences):
            complete_sentence = "(" + complete_sentence  + "&" + sentences[i] + ")"
            i += 1
        return TruthTable(complete_sentence)

    def create_truth_table_for_new_sentence(self, sentence, reward):
        # All variables found in the conjuction parts of the sentence, is need to be able to add non available variables, if closed world assumption is active
        available_variables = []

        for proposition in sentence.propositions[0][0]:
            available_variables.append(proposition.variable)
        # If closed world assumption is set to true, for not available fact, it will be assumed that the negation holds
        # i.e if D is not in the setence, !D is assumed
        # Otherwise (D v !D) is assumed, but (D v !D) is always true and can be ignored
        if self.closed_world_assumption:
            all_proposition_variable_names = get_variable_names_for_propositions()
            for proposition in all_proposition_variable_names:
                if not available_variables.__contains__(proposition) and not available_variables.__contains__("!" + proposition):
                    available_variables.append("!"+proposition )

        # Combine variables by conjunction
        conjuction_part =available_variables[0].replace("!", "") if "!" in available_variables[0] else "!"+ available_variables[0]
        i = 1
        while i < len(available_variables):
            conjuction_part = "(" + conjuction_part  + "|" + available_variables[i].replace("!", "") + ")" if "!" in available_variables[i] else "(" + conjuction_part  + "|" + "!"+ available_variables[i] + ")"
            i += 1
        complete_sentence = ("((" + conjuction_part + ")" + "|" + reward + ")")

        return TruthTable(complete_sentence)

     # Does the Belief Base entails  the New Sentence?
    def belief_base_infers_sentence(self, belief_base_truth_table, sentence_truth_table):
        # Get all indicies for which generated truth table of the belief base is true
        indices_for_truth_evaluation = [bin(i)[2:] for i, x in enumerate(belief_base_truth_table.outputs) if x == 1]
        # Get the variable ordering from sentence truth table by belief base truth table
        variable_ordering = []
        for variable in sentence_truth_table.variables:
            if variable in belief_base_truth_table.variables:
                variable_ordering.append(belief_base_truth_table.variables.index(variable))
            else:
                # New sentence has a variable which is not in belief base yet, we dont need to care about that value and add both 0 and 1
                variable_ordering.append("*")
        # Calculate output of sentence truth table to check if B -> phi
        for row_for_truth_evaluation in indices_for_truth_evaluation:
            # Add leading zeros
            row_for_truth_evaluation = row_for_truth_evaluation.zfill(len(belief_base_truth_table.variables))
            output_str = ""
            for variable_index in variable_ordering:
                if variable_index == "*":
                    output_str = output_str + '*'
                else:
                    output_str = output_str + str(row_for_truth_evaluation[variable_index])
            # Check if sentence truth table evaluates the values to true, If * use 0 and 1 once -> need to be true for all
            # B entails phi means -> for ß -> phi, and this is true if for value ß = 1 also phi needs to be 1
            if sentence_truth_table.get_output(output_str.replace('*', '0')) == 0 or sentence_truth_table.get_output(output_str.replace('*', '1')) == 0:
                # For any vlaue where ß is true, phi is false, so B does not entail phi
                return False
        return True

    def update_policy(self, reward, next_observation, next_available_sentences, current_health):
        # No need to update policy for that kind of decision making
        pass

class QLearningDecisionMakingSystem:

    def __init__(self, decision_making_system_args):
        self.reward_table = {
            Reward.toxic: int(decision_making_system_args[1]),
            Reward.nontoxic: int(decision_making_system_args[2])
        }
        self.use_recent_health = decision_making_system_args[0]
        self.reward_for_exploration = int(decision_making_system_args[3])
        self.learning_rate = float(decision_making_system_args[4])
        self.discount_factor = float(decision_making_system_args[5])
        self.q_table = {}
        self.exploration_probability = float(decision_making_system_args[6])
        self.last_action_chosen = None
        self.last_state_key = None

    def make_decision(self, observations, available_sentences, recent_health):
        key = self.create_key(observations, available_sentences, recent_health)
        if self.last_state_key == key:
            return self.last_action_chosen
        if key not in self.q_table:
            self.add_state(key)
        
        choice = random.choices(population=["BestAction", "Random"], weights=[1-self.exploration_probability, self.exploration_probability], k=1)
        if choice[0] == "BestAction":
            max_value = max(self.q_table[key].items(), key=lambda x: x[1])
            list_of_actions = []
            for action, reward in self.q_table[key].items():
                if reward == max_value[1]:
                    list_of_actions.append(action)
            action = random.choice(list_of_actions)
        else:
            action = random.choice(list(self.q_table[key].keys()))
        self.last_action_chosen = action
        self.last_state_key = key
        return action

    def add_state(self, key):
        self.q_table[key] = {Action.eat:0, Action.explore:0}

    def create_key(self, observations, available_sentences, recent_health):
        longest_observation = None
        for observation in observations:
            if longest_observation is None or len(observation.propositions[0][0]) > len(longest_observation.propositions[0][0]):
                longest_observation = observation
        key = "O:"
        for proposition in longest_observation.propositions[0][0]:
            key = key + proposition.variable
        key = key + "|B:"

        for sentence in available_sentences:
            for or_sentence in sentence.propositions:
                for proposition in or_sentence[0]:
                    key = key + proposition.variable
                key = key + "-"    
                key = key + or_sentence[1].value
                key = key + ","
        key = key[:-1]
        if self.use_recent_health:
           key = key + "|" + recent_health.value 
        return key

 
    def update_policy(self, reward, next_observation, next_available_sentences, recent_health):
        if len(self.q_table.keys()) == 0:
            return
        else:
            if not self.last_state_key:
                key = self.create_key(next_observation, next_available_sentences, recent_health)
                self.add_state(key)
            reward = self.reward_table.get(reward) if reward in self.reward_table else self.reward_for_exploration
            next_state = self.create_key(next_observation, next_available_sentences, recent_health)
            maximum_future_reward = self.get_maximum_reward_for_next_sate(next_state)

        self.q_table[self.last_state_key][self.last_action_chosen] = ((1-self.learning_rate) * self.q_table[self.last_state_key][self.last_action_chosen] +
         self.learning_rate * (reward + self.discount_factor * maximum_future_reward))

    def get_maximum_reward_for_next_sate(self, next_state):
        maximum_reward = 0
        if next_state not in self.q_table:
            self.add_state(next_state)
            return 0
        actions = self.q_table[next_state]
        for action, reward in actions.items():
            if reward > maximum_reward:
                maximum_reward = reward
        return maximum_reward

