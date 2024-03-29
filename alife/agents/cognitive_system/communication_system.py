from .propositions import *
import math
import copy 

class CommunicationSystem:

    def __init__(self, belief_revision_system, commuication_system_args):
        self.belief_revision_system = belief_revision_system
        self.able_to_communicate = commuication_system_args[0]
        if self.able_to_communicate:
            self.percentage_of_sentences_to_be_used = int(commuication_system_args[1])
            self.evidence_interpretation = commuication_system_args[2]


    def filter_sentences(self, other_agents_available_knowledge):
        if self.evidence_interpretation == EvidenceInterpretation.ranking.value:
            other_agents_available_knowledge.sort(key=lambda sentence: sentence.evidence, reverse=False)
        else:
            other_agents_available_knowledge.sort(key=lambda sentence: sentence.evidence, reverse=True)

        # Just take first n sentences
        total_amount_of_sentences = len(other_agents_available_knowledge)
        amount_of_sentences_to_return = math.ceil(total_amount_of_sentences /100 * self.percentage_of_sentences_to_be_used)
        sentences_from_communcication = []
        for sentence in other_agents_available_knowledge:
            if len(sentences_from_communcication) < amount_of_sentences_to_return or sentences_from_communcication[-1].evidence == sentence.evidence:
                sentence_from_communcication = copy.deepcopy(sentence)
                sentence_from_communcication.evidence = sentence.evidence
                sentences_from_communcication.append(copy.deepcopy(sentence))
            else:
                break
        return sentences_from_communcication


    def communicate(self, own_knowledge, other_agents_available_knowledge):
        senteces_for_revision = self.filter_sentences(other_agents_available_knowledge)
        revised_belief_base = own_knowledge
        for sentence in senteces_for_revision:
            revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], revised_belief_base);
        return revised_belief_base


