from .propositions import *

class LongTermMemory:

    def __init__(self):
        self.time_since_initialization = 1
        self.stored_sentences = []

    def get_time_since_initialization(self):
        return self.time_since_initialization

    def set_time_since_initialization(self, time_since_initialization):
        self.time_since_initialization = time_since_initialization

    def save_sentence(self, sentence_to_store: Sentence):
        sentence_to_store.usages = [self.time_since_initialization]
        self.stored_sentences.append(sentence_to_store)
        self.time_since_initialization = self.time_since_initialization + 1

    def update(self, revised_knowledge_base):
        updated_stored_sentences = []
        for sentence in revised_knowledge_base:
            if sentence in self.stored_sentences:
                sentence.usages.append(self.time_since_initialization)
                self.time_since_initialization = self.time_since_initialization + 1
                updated_stored_sentences.append(sentence)
            else:
                sentence.usages = [self.time_since_initialization]
                updated_stored_sentences.append(sentence)
                self.time_since_initialization = self.time_since_initialization + 1
        self.stored_sentences = updated_stored_sentences
        