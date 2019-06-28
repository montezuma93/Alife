from unittest import TestCase
from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import *
from .propositions import *

class ObservationToPropositionSystemTest(TestCase):

    def test_multiple_proposition_system(self):
        self.observation_to_proposition_system = MultiplePropositionSystem()
        observed_propositions = [NextToRock(), NextToTreeTrunk(), DayProposition()]
        color_proposition = ColorGreen()

        possible_propositions = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(8, len(possible_propositions))
        for possible_proposition in possible_propositions:
            self.assertTrue(possible_proposition[0].__contains__(color_proposition))
        for possible_proposition in possible_propositions:
            self.assertEqual(Reward.toxic, possible_proposition[1].reward)
            self.assertEqual(0.125, possible_proposition[1].evidence)
    
    def test_occams_razor_multiple_proposition_system(self):
        self.observation_to_proposition_system = OccamsRazorMultiplePropositionSystem() 
        observed_propositions = [NextToRock(), NextToTreeTrunk(), DayProposition()]
        color_proposition = ColorGreen()
        expected_evidence = {1:0.2,2:0.15,3:0.1,4:0.05}
        possible_propositions = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(8, len(possible_propositions))
        for possible_proposition in possible_propositions:
            self.assertTrue(possible_proposition[0].__contains__(color_proposition))
            self.assertEqual(Reward.toxic, possible_proposition[1].reward)
            self.assertAlmostEqual(expected_evidence.get(len(possible_proposition[0])), possible_proposition[1].evidence)
        

    def test_single_proposition_system(self):     
        self.observation_to_proposition_system = SinglePropositionSystem() 
        next_to_rock_proposition = NextToRock()
        next_to_tree_trunk_proposition = NextToTreeTrunk()
        day_proposition = DayProposition()
        color_proposition = ColorGreen()
        observed_propositions = [next_to_rock_proposition, next_to_tree_trunk_proposition, day_proposition]

        possible_propositions = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(1, len(possible_propositions))
        possible_proposition = possible_propositions[0]
        self.assertEqual(4, len(possible_proposition[0]))
        self.assertTrue(possible_proposition[0].__contains__(color_proposition))
        self.assertTrue(possible_proposition[0].__contains__(next_to_rock_proposition))
        self.assertTrue(possible_proposition[0].__contains__(next_to_tree_trunk_proposition))
        self.assertTrue(possible_proposition[0].__contains__(day_proposition))
        self.assertEqual(Reward.toxic, possible_proposition[1].reward)
        self.assertEqual(1, possible_proposition[1].evidence)

    def test_random_single_proposition_system(self): 
        self.observation_to_proposition_system = RandomSinglePropositionSystem()     
        observed_propositions = [NextToRock(), NextToTreeTrunk(), DayProposition()]
        color_proposition = ColorGreen()

        possible_propositions = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(1, len(possible_propositions))
        possible_proposition = possible_propositions[0]
        self.assertTrue(len(possible_proposition[0]) >= 1 and len(possible_proposition[0]) <= 5)
        self.assertTrue(possible_proposition[0].__contains__(color_proposition))
        self.assertEqual(Reward.toxic, possible_proposition[1].reward)
        self.assertEqual(1, possible_proposition[1].evidence)

