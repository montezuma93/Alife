from .propositions import *
from .long_term_memory import LongTermMemory
import copy
import math
import operator
import random

# See: Towards agents with human-like decisions under uncertainty
class HumanLikeDecisionMakingUnderUncertaintySystem:

    def __init__(self, risk_aversion):
        self.risk_aversion = risk_aversion
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
            "eat nontoxic":"eat",
            "eat toxic":"not eat"
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
            weightning = ((self.delta + 0.5 - self.risk_aversion) * math.pow(weightning_table[key],self.gamma))
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


    def normalize_sentences(self, sentences_to_normalize):
        sentences = []
        total_weight = sum([sentence.evidence for sentence in sentences_to_normalize])
        for sentence in sentences_to_normalize:
            normalized_sentence = copy.copy(sentence)
            normalized_sentence.evidence = sentence.evidence / total_weight
            sentences.append(normalized_sentence)
        return sentences



class QLearningDecisionMakingSystem:

    def __init__(self):
        self.q_table = {}
        self.exploration_probability = 0

    def make_decision(self, observations, available_sentences):
        key = self.create_key(observations, available_sentences)
        if key not in self.q_table:
            self.q_table[key] = {"Eat":0, "NotEat":0}
        
        choice = random.choices(population=["BestAction", "Random"], weights=[1-self.exploration_probability, self.exploration_probability], k=1)

        if choice[0] == "BestAction":
            return max(self.q_table[key].items(), key=operator.itemgetter(1))[0]
        else:
            return random.choice(list(self.q_table[key].keys()))

    def create_key(self, observations, available_sentences):
        longest_observation = []
        for observation in observations:
            if len(observation) > len(longest_observation):
                longest_observation = observation
        key = "O:"
        for proposition in longest_observation:
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
 
