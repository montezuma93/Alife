from unittest import TestCase
from .decision_making_system import HumanLikeDecisionMakingUnderUncertaintySystem, QLearningDecisionMakingSystem
from .propositions import *
 

class HumanLikeDecisionMakingUnderUncertaintySystemTest(TestCase):
 
    def test_normalize_available_sentences(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem(0)

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic)], 0.1)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([NightProposition(), ColorGreen()], Reward.nontoxic)], 0.3)
        sentence_4 = Sentence([([NextToRock(), DayProposition(), ColorBlue()], Reward.toxic)], 0.4)
        sentence_5 = Sentence([([NextToRock(), NightProposition(), ColorBlue()], Reward.nontoxic)], 0.5)

        normalized_sentences = self.decision_making_system.normalize_sentences([sentence_1, sentence_2, sentence_3, sentence_4, sentence_5])

        self.assertEqual(1, sum([sentence.evidence for sentence in normalized_sentences]))
        self.assertEqual(0.1, sentence_1.evidence)
        self.assertAlmostEqual(0.06666666, normalized_sentences[0].evidence)
        self.assertAlmostEqual(0.1333333, normalized_sentences[1].evidence)
        self.assertAlmostEqual(0.199999999, normalized_sentences[2].evidence)
        self.assertAlmostEqual(0.266666666, normalized_sentences[3].evidence)
        self.assertAlmostEqual(0.33333333, normalized_sentences[4].evidence)
        
    def test_make_decision(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem(1)

        sentence_1 = Sentence([([ColorGreen()], Reward.nontoxic)], 0.1)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.3)
        sentence_4 = Sentence([([NextToRock(), DayProposition(), ColorBlue()], Reward.toxic)], 0.4)
        sentence_5 = Sentence([([NextToRock(), NightProposition(), ColorBlue()], Reward.nontoxic)], 0.5)

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5])
        self.assertEqual("eat", action)

    def test_make_decision_evidence_it_is_toxic(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem(0)

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)
        sentence_4 = Sentence([([NextToRock(), DayProposition(), ColorBlue()], Reward.nontoxic)], 0.1)
        sentence_5 = Sentence([([NextToRock(), NightProposition(), ColorBlue()], Reward.nontoxic)], 0.5)

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5])

        self.assertEqual("eat", action)

    def test_make_decision_evidence_it_is_toxic_with_risk_aversion(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem(1)

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)
        sentence_4 = Sentence([([NextToRock(), DayProposition(), ColorBlue()], Reward.nontoxic)], 0.1)
        sentence_5 = Sentence([([NextToRock(), NightProposition(), ColorBlue()], Reward.nontoxic)], 0.5)

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5])
        self.assertEqual("eat", action)


        "TODO INCLUDE OR TEST"



    def test_create_key(self):
        self.decision_making_system = QLearningDecisionMakingSystem()

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        key =  self.decision_making_system.create_key(observations, [sentence_1, sentence_2, sentence_3])
        self.assertEqual("O:GRD|B:G-X,G!D-X,RTG-X,DG-!X", key)



    def test_make_decision(self):
        self.decision_making_system = QLearningDecisionMakingSystem()
        self.decision_making_system.q_table = {
            "O:GRD|B:G-X,G!D-X,RTG-X,DG-!X":{
                "Eat":0.1,
                "NotEat":0.2
            }
        }
        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3])
        self.assertEqual("NotEat", action)
