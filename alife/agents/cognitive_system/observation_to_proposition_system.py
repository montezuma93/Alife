import itertools
from.propositions import *
class OberservationToPropositionSystem:


    def __init__(self, multiple_propositions_allowed):
        self.multiple_propositions_allowed = multiple_propositions_allowed

    def observation_to_proposition(self, color_proposition: ColorProposition, observated_objects: list, reward: Reward):
        generated_propositions = []
        generated_propositions.append(([color_proposition], reward))
        combinations = []
        for i in range(1, len(observated_objects)+1):
            next_list = [list(x) for x in itertools.combinations(observated_objects, i)]
            for entry in next_list:
                entry.append(color_proposition)
                generated_propositions.append((entry, reward))
        
        return generated_propositions


