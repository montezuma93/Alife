from .propositions import *

class LongTermMemory:


    def __init__(self):
        self.time_since_initialization = 1
        self.stored_sentences = []


    def save_sentence(self, sentence_to_store: Sentence):
        sentence_to_store.usages = [self.time_since_initialization]
        self.stored_sentences.append(sentence_to_store)
        self.time_since_initialization = self.time_since_initialization + 1

    def update(self, revised_knowledge_base):
        pass