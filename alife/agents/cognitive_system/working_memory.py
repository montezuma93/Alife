from .propositions import *
from .long_term_memory import LongTermMemory
import math
from numpy import log, power


class WorkingMemoryWithEvidence:

    def __init__(self):
        #Between 1 and 100
        self.percentage_amount_for_retrieving = 10

    def set_percentage_amount_for_retrieving(self, percentage_amount_for_retrieving):
        if percentage_amount_for_retrieving < 1 or percentage_amount_for_retrieving > 100:
            return
        self.percentage_amount_for_retrieving = percentage_amount_for_retrieving

    def retrieve_knowledge(self, new_sentence: Sentence, stored_sentences: list):
        stored_sentences.sort(key=lambda sentence: sentence.evidence, reverse=True)
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

    def __init__(self):
        self.initial_activation_value = 1
        self.base_activation_decay = -0.5
        self.include_percentage_evidence_value = 0

    def set_include_percentage_evidence_value(self, include_percentage_evidence_value):
        self.include_percentage_evidence_value = include_percentage_evidence_value

    def retrieve_knowledge(self, new_sentence: Sentence, stored_sentences: list, actual_time_step: int):
        self.init_activation_value_property(stored_sentences)
        if new_sentence:
            self.spread_activation(new_sentence, stored_sentences)
        self.add_calculated_base_activation(stored_sentences, actual_time_step)
        if self.include_percentage_evidence_value > 0:
            self.add_evidence_to_activation_value(stored_sentences)
        retrieval_threshold = self.calculate_threshold(stored_sentences)
        available_sentences = self.get_most_activated_sentences(stored_sentences, retrieval_threshold)
        return available_sentences

    def init_activation_value_property(self, stored_sentences):
        for sentence in stored_sentences:
            sentence.activation_value = 0

    def spread_activation(self, new_sentence: Sentence, stored_sentences: list):
        if new_sentence:
            for proposition in new_sentence.propositions[0][0]:
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
        for sentence in stored_sentences:
            evidence_acitvation_value = sentence.evidence /100*self.include_percentage_evidence_value
            sentence.activation_value = sentence.activation_value + evidence_acitvation_value
    
    def add_calculated_base_activation(self, stored_sentences, actual_time_step):
        for sentence in stored_sentences:
            sum_of_usages = 0
            for usage in sentence.usages:
                sum_of_usages += power((actual_time_step - usage), self.base_activation_decay)
            base_activation_value = log(sum_of_usages)
            sentence.activation_value = sentence.activation_value + base_activation_value

    def calculate_threshold(self, stored_sentences):
        total_activation_value = 0
        for sentence in stored_sentences:
            total_activation_value = total_activation_value + sentence.activation_value
        average_activation = total_activation_value/len(stored_sentences)
        return average_activation


    def get_most_activated_sentences(self, stored_sentences, retrieval_threshold):
        available_sentences = []
        for sentence in stored_sentences:
            if sentence.activation_value > retrieval_threshold:
                available_sentences.append(sentence)
        return available_sentences

