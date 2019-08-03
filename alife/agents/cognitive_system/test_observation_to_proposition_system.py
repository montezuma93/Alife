from unittest import TestCase
from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import *
from .propositions import *

class ObservationToPropositionSystemTest(TestCase):

    def test_multiple_proposition_system(self):
        self.observation_to_proposition_system = MultiplePropositionSystem([])
        observed_propositions = [NextToRock(), NextToTreeTrunk(), DayProposition()]
        color_proposition = ColorGreen()

        created_sentences = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(8, len(created_sentences))
        for sentence in created_sentences:
            self.assertTrue(sentence.propositions[0][0].__contains__(color_proposition))
        for sentence in created_sentences:
            self.assertEqual(Reward.toxic, sentence.propositions[0][1])
            self.assertEqual(0.125, sentence.evidence)
    
    def test_occams_razor_multiple_proposition_system(self):
        self.observation_to_proposition_system = OccamsRazorMultiplePropositionSystem([]) 
        observed_propositions = [NextToRock(), NextToTreeTrunk(), DayProposition()]
        color_proposition = ColorGreen()
        expected_evidence = {1:0.2,2:0.15,3:0.1,4:0.05}

        created_sentences = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(8, len(created_sentences))
        for sentence in created_sentences:
            self.assertTrue(sentence.propositions[0][0].__contains__(color_proposition))
            self.assertEqual(Reward.toxic, sentence.propositions[0][1])
            self.assertAlmostEqual(expected_evidence.get(len(sentence.propositions[0][0])), sentence.evidence)
        

    def test_single_proposition_system(self):     
        self.observation_to_proposition_system = SinglePropositionSystem([]) 
        next_to_rock_proposition = NextToRock()
        next_to_tree_trunk_proposition = NextToTreeTrunk()
        day_proposition = DayProposition()
        color_proposition = ColorGreen()
        observed_propositions = [next_to_rock_proposition, next_to_tree_trunk_proposition, day_proposition]

        created_sentences = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(1, len(created_sentences))
        sentence = created_sentences[0]
        self.assertEqual(4, len(sentence.propositions[0][0]))
        self.assertTrue(sentence.propositions[0][0].__contains__(color_proposition))
        self.assertTrue(sentence.propositions[0][0].__contains__(next_to_rock_proposition))
        self.assertTrue(sentence.propositions[0][0].__contains__(next_to_tree_trunk_proposition))
        self.assertTrue(sentence.propositions[0][0].__contains__(day_proposition))
        self.assertEqual(Reward.toxic, sentence.propositions[0][1])
        self.assertEqual(1, sentence.evidence)

    def test_random_single_proposition_system(self): 
        self.observation_to_proposition_system = RandomSinglePropositionSystem([])     
        observed_propositions = [NextToRock(), NextToTreeTrunk(), DayProposition()]
        color_proposition = ColorGreen()

        created_sentences = self.observation_to_proposition_system.observation_to_proposition(color_proposition, observed_propositions, Reward.toxic)

        self.assertEqual(1, len(created_sentences))
        sentence = created_sentences[0]
        self.assertTrue(len(sentence.propositions[0][0]) >= 1 and len(sentence.propositions[0][0]) <= 5)
        self.assertTrue(sentence.propositions[0][0].__contains__(color_proposition))
        self.assertEqual(Reward.toxic, sentence.propositions[0][1])
        self.assertEqual(1, sentence.evidence)
