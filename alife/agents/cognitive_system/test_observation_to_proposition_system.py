from unittest import TestCase
from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import OberservationToPropositionSystem
from .propositions import *

class ObservationToPropositionSystemTest(TestCase):

    def setUp(self):
        self.observation_to_proposition_system = OberservationToPropositionSystem(True)

    def test_create_multiple_propositions_form_observation(self):      
        observed_propositions = [NextToRock(), NextToTreeTrunk(), DayProposition()]
        color_proposition = ColorGreen()

        possible_propositions = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(8, len(possible_propositions))
        for possible_proposition in possible_propositions:
            self.assertTrue(possible_proposition[0].__contains__(color_proposition))
        for possible_proposition in possible_propositions:
            self.assertEqual(Reward.toxic, possible_proposition[1])
