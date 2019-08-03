from .propositions import *
from .action import Action
from .long_term_memory import LongTermMemory
import copy
import math
import operator
import random
# See: Towards agents with human-like decisions under uncertainty
class HumanLikeDecisionMakingUnderUncertaintySystem:

    def __init__(self, decision_making_system_args):
        self.risk_aversion = int(decision_making_system_args[0])
        self.epsilon = 0.001
        self.delta = 0.77
        self.gamma = 0.44

    # Observation = [Proposition,...], [...]
    def make_decision(self, observations, available_sentences):
        utility_table = {
            "eat nontoxic":10,
            "eat toxic":1
        }
        weightning_table = {
            "eat nontoxic":0,
            "eat toxic":0
        }
        solution_table = {
            "eat nontoxic":0, # eat
            "eat toxic":0 # not eat
        }
        solution_to_action_mapping = {
            "eat nontoxic": Action.move_towards,
            "eat toxic": Action.move_elsewhere
        }
        sentences = self.normalize_sentences(available_sentences)
        evidence_for_toxic = 0
        evidence_for_non_toxic = 0
        for observation in observations:
            for sentence in sentences:
                is_in_sentence = self.observation_is_in_sentence(observation, sentence)
                if is_in_sentence:
                    # TODO For Each Or Part differently
                    if sentence.propositions[0][1] == Reward.toxic:
                        evidence_for_toxic = evidence_for_toxic + sentence.evidence
                    else:
                        evidence_for_non_toxic = evidence_for_non_toxic + sentence.evidence
        weightning_table["eat nontoxic"] = evidence_for_non_toxic if evidence_for_non_toxic > 0 else self.epsilon
        weightning_table["eat toxic"] = evidence_for_toxic if evidence_for_toxic > 0 else self.epsilon

        for key in solution_table.keys():
            utility = utility_table[key]
            weightning = ((self.delta + 0.5 - self.risk_aversion) * math.pow(weightning_table[key],self.gamma)) / (
                ((self.delta + 0.5 - self.risk_aversion) * math.pow(weightning_table[key],self.gamma)) +  math.pow((1-weightning_table[key]),self.gamma))
            solution_table[key] = utility * weightning
        return solution_to_action_mapping.get(max(solution_table.items(), key=operator.itemgetter(1))[0])

    def observation_is_in_sentence(self, observation, sentence):
        for or_sentences in sentence.propositions:
            if len(or_sentences[0]) != len(observation):
                return False
            for observation_proposition in observation:
                if not any(isinstance(sentence_proposition, type(observation_proposition)) for sentence_proposition in or_sentences[0]):
                    break
            else:
                return True
        else:
            return False

    # Heighest value should be 1- epsilon
    def normalize_sentences(self, sentences_to_normalize):
        sentences = []
        if len(sentences_to_normalize) > 0:
            max_value = max([sentence.evidence for sentence in sentences_to_normalize])
            dividing_factor = max_value / (1-self.epsilon)
            for sentence in sentences_to_normalize:
                normalized_sentence = copy.copy(sentence)
                normalized_sentence.evidence = sentence.evidence / dividing_factor
                sentences.append(normalized_sentence)
        return sentences

    def update_policy(self, reward, next_observation, next_available_sentences):
        # No need to update policy for that kind of decision making
        pass

class QLearningDecisionMakingSystem:

    def __init__(self):
        self.reward_table = {
            Reward.toxic: -10,
            Reward.nontoxic: 10
        }
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.q_table = {}
        self.exploration_probability = 0
        self.last_action_chosen = None
        self.last_state_key = None

    def make_decision(self, observations, available_sentences):
        key = self.create_key(observations, available_sentences)
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
        self.q_table[key] = {Action.move_towards:0, Action.move_elsewhere:0}

    def create_key(self, observations, available_sentences):
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
        return key[:-1]
 
    def update_policy(self, reward, next_observation, next_available_sentences):
        if not self.last_state_key:
            key = self.create_key(next_observation, next_available_sentences)
            self.add_state(key)
        reward = self.reward_table.get(reward)
        next_state = self.create_key(next_observation, next_available_sentences)
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
