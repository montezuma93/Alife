from unittest import TestCase
from .decision_making_system import HumanLikeDecisionMakingUnderUncertaintySystem, QLearningDecisionMakingSystem
from .propositions import *
from .action import *
 

class DecisionMakingSystemTest(TestCase):

####################################### HUMAN LIKE DECISION MAKING UNDER UNCERTAINTY SYSTEM  ##############################

    def test_normalize_available_sentences(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([0])

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic)], 4)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 3)
        sentence_3 = Sentence([([NightProposition(), ColorGreen()], Reward.nontoxic)], 1)
        sentence_4 = Sentence([([NextToRock(), DayProposition(), ColorBlue()], Reward.toxic)], 0.1)

        normalized_sentences = self.decision_making_system.normalize_sentences([sentence_1, sentence_2, sentence_3, sentence_4])

        self.assertEqual(4, sentence_1.evidence)
        self.assertAlmostEqual(4/ (4/(1-self.decision_making_system.epsilon)), normalized_sentences[0].evidence)
        self.assertAlmostEqual(0.74925, normalized_sentences[1].evidence)
        self.assertAlmostEqual(0.24975, normalized_sentences[2].evidence)
        self.assertAlmostEqual(0.024975, normalized_sentences[3].evidence)

    def test_make_decision(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([1])

        sentence_1 = Sentence([([ColorGreen()], Reward.nontoxic)], 0.1)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.3)
        sentence_4 = Sentence([([NextToRock(), DayProposition(), ColorBlue()], Reward.toxic)], 0.4)
        sentence_5 = Sentence([([NextToRock(), NightProposition(), ColorBlue()], Reward.nontoxic)], 0.5)

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5])
        self.assertEqual(Action.move_towards, action)

    def test_make_decision_evidence_it_is_toxic(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([0])

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)
        sentence_4 = Sentence([([NextToRock(), DayProposition(), ColorBlue()], Reward.nontoxic)], 0.1)
        sentence_5 = Sentence([([NextToRock(), NightProposition(), ColorBlue()], Reward.nontoxic)], 0.5)

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5])

        self.assertEqual(Action.move_towards, action)

    def test_make_decision_evidence_it_is_toxic_with_risk_aversion(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([1])

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)
        sentence_4 = Sentence([([NextToRock(), DayProposition(), ColorBlue()], Reward.nontoxic)], 0.1)
        sentence_5 = Sentence([([NextToRock(), NightProposition(), ColorBlue()], Reward.nontoxic)], 0.5)

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5])
        self.assertEqual(Action.move_towards, action)

    def test_make_decision_evidence_with_empty_knowledge_base(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([0])

        observations = [[ColorGreen(), NextToRock(), DayProposition()], [ColorGreen(), NextToRock()], [ColorGreen(), DayProposition()], [ColorGreen()]]

        action = self.decision_making_system.make_decision(observations, [])
        self.assertEqual(Action.move_towards, action)



####################################### Q LEARNING SYSTEM  ##############################
    

    def test_create_key(self):
        self.decision_making_system = QLearningDecisionMakingSystem()

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        key =  self.decision_making_system.create_key(observations, [sentence_1, sentence_2, sentence_3])
        self.assertEqual("O:GRD|B:G-X,G!D-X,RTG-X,DG-!X", key)

    def test_make_decision(self):
        self.decision_making_system = QLearningDecisionMakingSystem()
        self.decision_making_system.q_table = {
            "O:GRD|B:G-X,G!D-X,RTG-X,DG-!X":{
                Action.move_towards:0.1,
                Action.move_elsewhere:0.2
            }
        }
        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3])
        self.assertEqual(Action.move_elsewhere, action)

    

    def test_make_decision_with_empty_q_table_same_following_state(self):
        self.decision_making_system = QLearningDecisionMakingSystem()

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        available_knowledge = [sentence_1, sentence_2, sentence_3]
        
        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        self.decision_making_system.make_decision(observations, available_knowledge)
        self.decision_making_system.update_policy(10, observations, available_knowledge)

        self.assertEqual(1, len(self.decision_making_system.q_table))
        self.assertEqual(1, max(self.decision_making_system.q_table["O:GRD|B:G-X,G!D-X,RTG-X,DG-!X"].items(), key=lambda x: x[1])[1])

    def test_make_decision_with_empty_q_table_same_following_state(self):
        self.decision_making_system = QLearningDecisionMakingSystem()

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        available_knowledge = [sentence_1, sentence_2, sentence_3]
        
        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        self.decision_making_system.make_decision(observations, available_knowledge)


        next_observations = [Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]
        
        self.decision_making_system.update_policy(10, next_observations, available_knowledge)

        self.assertEqual(2, len(self.decision_making_system.q_table))
        self.assertEqual(1, max(self.decision_making_system.q_table["O:GRD|B:G-X,G!D-X,RTG-X,DG-!X"].items(), key=lambda x: x[1])[1])
        self.assertEqual(0, max(self.decision_making_system.q_table["O:GD|B:G-X,G!D-X,RTG-X,DG-!X"].items(), key=lambda x: x[1])[1])