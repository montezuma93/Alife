from unittest import TestCase
from .communication_system import CommunicationSystem
from .propositions import *
from .belief_revision_system import *

class CommunicationSystemTest(TestCase):

    def test_save_sentences(self):

        self.belief_revision_system = FormalBeliefRevision([True])
        self.communication_system = CommunicationSystem(self.belief_revision_system, [True, 10, EvidenceInterpretation.evidence.value])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)

        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 2)
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 3)
        self.assertEqual(5, len(self.communication_system.communicate([sentence_1, sentence_2], [sentence_3])))