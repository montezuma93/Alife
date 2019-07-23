from unittest import TestCase
from .long_term_memory import LongTermMemory
from .propositions import *
 

class LongTermMemoryTest(TestCase):
 
    def setUp(self):
 
        self.long_term_memory = LongTermMemory()
 
    def test_save_sentences(self):

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1)
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)

        self.long_term_memory.save_sentence(sentence_1)

        self.assertEqual(1, len(self.long_term_memory.stored_sentences))
        self.assertEqual(sentence_1, self.long_term_memory.stored_sentences[0])
        self.assertEqual(1, self.long_term_memory.stored_sentences[0].usages[0])

        self.long_term_memory.save_sentence(sentence_2)

        self.assertEqual(2, len(self.long_term_memory.stored_sentences))
        self.assertEqual(sentence_2, self.long_term_memory.stored_sentences[1])
        self.assertEqual(2, self.long_term_memory.stored_sentences[1].usages[0])

        self.long_term_memory.save_sentence(sentence_3)

        self.assertEqual(3, len(self.long_term_memory.stored_sentences))
        self.assertEqual(sentence_3, self.long_term_memory.stored_sentences[2])
        self.assertEqual(3, self.long_term_memory.stored_sentences[2].usages[0])


