import itertools
from.propositions import *
import random
class OberservationToPropositionSystem:

    def __init__(self):
        pass

class MultiplePropositionSystem(OberservationToPropositionSystem):

    def __init__(self, observation_system_args):
        pass
    
    def observation_to_proposition(self, color_proposition: ColorProposition, observated_objects: list, reward: Reward):
        amount_of_combinations = {1:2,2:4,3:8}
        evidence = 1/amount_of_combinations.get(len(observated_objects))

        generated_propositions = []
        generated_propositions.append(Sentence([([color_proposition], reward)], evidence))
        combinations = []
        for i in range(1, len(observated_objects)+1):
            next_list = [list(x) for x in itertools.combinations(observated_objects, i)]
            for entry in next_list:
                entry.append(color_proposition)
                generated_propositions.append(Sentence([(entry, reward)], evidence))
        
        return generated_propositions


class OccamsRazorMultiplePropositionSystem(OberservationToPropositionSystem):
    
    def __init__(self, observation_system_args):
        pass
    
    def observation_to_proposition(self, color_proposition: ColorProposition, observated_objects: list, reward: Reward):
        max_length_of_proposition = {0:1,1:2,2:3,3:4}
        total_length_of_combination = {0:1,1:3,2:8,3:20}
        evidence_per_combination_part = 1/total_length_of_combination.get(len(observated_objects))
        generated_propositions = []
        generated_propositions.append(Sentence([([color_proposition], reward)], evidence_per_combination_part*(max_length_of_proposition.get(len(observated_objects)))))
        for i in range(1, len(observated_objects)+1):
            next_list = [list(x) for x in itertools.combinations(observated_objects, i)]
            for entry in next_list:
                entry.append(color_proposition)
                generated_propositions.append(Sentence([(entry, reward)], evidence_per_combination_part*(max_length_of_proposition.get(len(observated_objects))-len(entry)+1)))
        return generated_propositions

class SinglePropositionSystem(OberservationToPropositionSystem):
    
    def __init__(self, observation_system_args):
        pass
    
    def observation_to_proposition(self, color_proposition: ColorProposition, observated_objects: list, reward: Reward):
        evidence = 1
        observated_objects.append(color_proposition)

        return [Sentence([(observated_objects, reward)], evidence)]

class RandomSinglePropositionSystem(OberservationToPropositionSystem):
    
    def __init__(self, observation_system_args):
        pass
    
    def observation_to_proposition(self, color_proposition: ColorProposition, observated_objects: list, reward: Reward):
        evidence = 1
        generated_propositions = []
        generated_propositions.append(Sentence([([color_proposition], reward)], evidence))
        combinations = []
        for i in range(1, len(observated_objects)+1):
            next_list = [list(x) for x in itertools.combinations(observated_objects, i)]
            for entry in next_list:
                entry.append(color_proposition)
                generated_propositions.append(Sentence([(entry, reward)], evidence))
        
        return [random.choice(generated_propositions)]
