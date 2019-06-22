from unittest import TestCase
from .long_term_memory import LongTermMemory
from .propositions import *
 

class LongTermMemoryTest(TestCase):
 
    def setUp(self):
 
        self.long_term_memory = LongTermMemory()
 
 
    def test_store(self):
 
        proposition_to_save = ColorGreen()
        self.long_term_memory.save_proposition(proposition_to_save)

        self.assertEqual(1, len(self.long_term_memory.stored_proposition[ColorProposition.__name__]))
        self.assertEqual(proposition_to_save, self.long_term_memory.stored_proposition[ColorProposition.__name__][0])