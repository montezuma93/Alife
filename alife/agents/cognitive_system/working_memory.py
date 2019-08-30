from .propositions import *
from .long_term_memory import LongTermMemory
import math
from numpy import log, power


class WorkingMemoryWithEvidence:

    def __init__(self, working_memory_system_args):
        #Between 1 and 100
        self.percentage_amount_for_retrieving = 100
        self.evidence_interpretation = working_memory_system_args[0]

    def set_percentage_amount_for_retrieving(self, percentage_amount_for_retrieving):
        if percentage_amount_for_retrieving < 1 or percentage_amount_for_retrieving > 100:
            return
        self.percentage_amount_for_retrieving = percentage_amount_for_retrieving

    def retrieve_knowledge(self, new_sentences: list, long_term_memory):
        stored_sentences = long_term_memory.stored_sentences
        if self.evidence_interpretation == EvidenceInterpretation.evidence.value or self.evidence_interpretation == EvidenceInterpretation.probability.value:
            stored_sentences.sort(key=lambda sentence: sentence.evidence, reverse=True)
        elif self.evidence_interpretation == EvidenceInterpretation.ranking.value:
            stored_sentences.sort(key=lambda sentence: sentence.evidence, reverse=False)
        else:
            print("No availaible Interpretation")
        total_amount_of_sentences = len(stored_sentences)
        amount_of_sentences_to_return = math.ceil(total_amount_of_sentences /100 * self.percentage_amount_for_retrieving)
        available_sentences = []
        for sentence in stored_sentences:
            if len(available_sentences) < amount_of_sentences_to_return or available_sentences[-1].evidence == sentence.evidence:
                available_sentences.append(sentence)
            else:
                break
        return available_sentences


class WorkingMemoryWithActivationSpreading:

    def __init__(self, working_memory_system_args):
        self.initial_activation_value = 1
        # Just used for evidence and probability interpretation
        self.base_activation_decay = -0.5
        # Percentage of evidence used
        # For probability factor to multiply proability with
        # For ranking penalty for rank
        self.include_percentage_evidence_value = 10
        self.evidence_interpretation = working_memory_system_args[0]

    def set_include_percentage_evidence_value(self, include_percentage_evidence_value):
        self.include_percentage_evidence_value = include_percentage_evidence_value

    def retrieve_knowledge(self, new_sentences: list, long_term_memory):
        stored_sentences = long_term_memory.stored_sentences
        actual_time_step = long_term_memory.get_time_since_initialization()
        self.init_activation_value_property(stored_sentences)
        if new_sentences:
            self.spread_activation(new_sentences, stored_sentences)
        # Just can calculate base activation for evidence and probability
        # For ranking function all sentences are in belief base with same storage time
        if self.evidence_interpretation == EvidenceInterpretation.evidence.value or self.evidence_interpretation == EvidenceInterpretation.probability.value:
            self.add_calculated_base_activation(stored_sentences, actual_time_step)
        if self.include_percentage_evidence_value > 0:
            self.add_evidence_to_activation_value(stored_sentences)
        retrieval_threshold = self.calculate_threshold(stored_sentences)
        available_sentences = self.get_most_activated_sentences(stored_sentences, retrieval_threshold)
        return available_sentences

    def init_activation_value_property(self, stored_sentences):
        for sentence in stored_sentences:
            sentence.activation_value = 0

    def spread_activation(self, new_sentences: list, stored_sentences: list):
        for sentence in new_sentences:
            for proposition in sentence.propositions[0][0]:
                sentence_receive_activation_fraction = []
                for sentence in stored_sentences:
                    if any(isinstance(x, type(proposition)) for x in sentence.propositions[0][0]):
                        sentence_receive_activation_fraction.append(sentence)
                # Add activation spreading to sentences
                if len(sentence_receive_activation_fraction) > 0:
                    activation_value_to_add = self.initial_activation_value/len(sentence_receive_activation_fraction)
                    for sentence in sentence_receive_activation_fraction:
                        sentence.activation_value = sentence.activation_value + activation_value_to_add

    def add_evidence_to_activation_value(self, stored_sentences):

        if self.evidence_interpretation == EvidenceInterpretation.evidence.value:
            for sentence in stored_sentences:
                evidence_acitvation_value = sentence.evidence /100 * self.include_percentage_evidence_value
                sentence.activation_value = sentence.activation_value + evidence_acitvation_value
        elif self.evidence_interpretation == EvidenceInterpretation.probability.value:
            for sentence in stored_sentences:
                probability_factor = sentence.evidence * self.include_percentage_evidence_value
                sentence.activation_value = sentence.activation_value + probability_factor
        elif self.evidence_interpretation == EvidenceInterpretation.ranking.value:
            for sentence in stored_sentences:
                ranking_factor = sentence.evidence * self.include_percentage_evidence_value
                sentence.activation_value = sentence.activation_value - ranking_factor
        else:
            print("No availaible Interpretation")
    
    def add_calculated_base_activation(self, stored_sentences, actual_time_step):
        for sentence in stored_sentences:
            sum_of_usages = 0
            for usage in sentence.usages:
                sum_of_usages += power((actual_time_step - usage), self.base_activation_decay)
            base_activation_value = log(sum_of_usages)
            sentence.activation_value = sentence.activation_value + base_activation_value

    def calculate_threshold(self, stored_sentences):
        if len(stored_sentences) == 0:
            return 0
        total_activation_value = 0
        for sentence in stored_sentences:
            total_activation_value = total_activation_value + sentence.activation_value
        average_activation = total_activation_value/len(stored_sentences)
        return average_activation


    def get_most_activated_sentences(self, stored_sentences, retrieval_threshold):
        available_sentences = []
        for sentence in stored_sentences:
            if sentence.activation_value >= retrieval_threshold:
                available_sentences.append(sentence)
        return available_sentences



