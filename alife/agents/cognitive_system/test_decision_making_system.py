from unittest import TestCase
from .decision_making_system import HumanLikeDecisionMakingUnderUncertaintySystem, QLearningDecisionMakingSystem
from .propositions import *
from .action import *
import math
 

class DecisionMakingSystemTest(TestCase):

####################################### HUMAN LIKE DECISION MAKING UNDER UNCERTAINTY SYSTEM  ##############################
    '''
    def test_make_decision_decision_evidence(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([1, 0, EvidenceInterpretation.evidence.value, False, False, 10, 10])

        sentence_1 = Sentence([([ColorGreen()], Reward.nontoxic)], 5)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 3)

        observations = [Sentence([([ColorGreen(), NextToRock()], Reward.none)], 1), Sentence([([ColorGreen()], Reward.none)], 1)]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3], Health.moreThanHalf)
        self.assertEqual(Action.explore, action)

    def test_make_decision_decision_probability(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([1,  0, EvidenceInterpretation.probability.value, False, False, 10, 10])

        sentence_1 = Sentence([([ColorGreen()], Reward.nontoxic)], 0.1)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([ColorGreen() ], Reward.toxic)], 0.3)

        observations = [Sentence([([ColorGreen(), NextToRock()], Reward.none)], 1), Sentence([([ColorGreen()], Reward.none)], 1)]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3])
        self.assertEqual(Action.explore, action)

    '''
    def test_make_decision_decision_ranking(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([1, 0,  EvidenceInterpretation.ranking.value, True, False, 10, 10])

        sentence_1 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.nontoxic)], 0)
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorOrange()], Reward.toxic)], 2)
        sentence_3 = Sentence([([ColorGreen() ], Reward.toxic)], 3)

        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 1), Sentence([([ColorGreen()], Reward.none)], 1)]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3], Health.lessThanHalf)
        self.assertEqual(Action.explore, action)
    '''
    def test_make_decision_decision_ranking(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([0.5, 0.5,  EvidenceInterpretation.ranking.value, False, True, 5, 10, 25, 50, 50,25,10,5])

        sentence_1 = Sentence([([ColorGreen()], Reward.nontoxic)], 0)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 2)
        sentence_3 = Sentence([([ColorGreen() ], Reward.toxic)], 3)

        observations = [Sentence([([ColorGreen(), NextToRock()], Reward.none)], 1), Sentence([([ColorGreen()], Reward.none)], 1)]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3], Health.lessThanQuarter)
        self.assertEqual(Action.eat, action)

    def test_make_decision_decision_ranking_with_health(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([0.5, 0.5,  EvidenceInterpretation.ranking.value, False, True,5, 10, 25, 50, 50,25,10,5])

        sentence_1 = Sentence([([ColorGreen()], Reward.nontoxic)], 0)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 2)
        sentence_3 = Sentence([([ColorGreen() ], Reward.toxic)], 3)

        observations = [Sentence([([ColorGreen(), NextToRock()], Reward.none)], 1), Sentence([([ColorGreen()], Reward.none)], 1)]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3], Health.moreThanHalf)
        self.assertEqual(Action.explore, action)


    def test_entropy(self):

        self.assertAlmostEqual(0.6931, (0.5 * math.log(0.5) + 0.5 * math.log(0.5)) * -1, 3)

    def test_make_decision_decision_probability(self):
        self.decision_making_system = HumanLikeDecisionMakingUnderUncertaintySystem([1,  1, EvidenceInterpretation.probability.value, False, False, 10, 10])
        self.decision_making_system.utility_table = {
            "eat":20,
            "explore":5
        }
        sentence_1 = Sentence([([ColorGreen()], Reward.nontoxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([ColorGreen() ], Reward.toxic)], 0.1)

        observations = [Sentence([([ColorGreen(), NextToRock()], Reward.none)], 1), Sentence([([ColorGreen()], Reward.none)], 1)]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3], Health.moreThanHalf)
        self.assertEqual(Action.eat, action)
        '''

####################################### Q LEARNING SYSTEM  ##############################
    def test_create_key(self):
        self.decision_making_system = QLearningDecisionMakingSystem([False, -10, 10, 1, 0.1, 0.9, 0.9])

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        key =  self.decision_making_system.create_key(observations, [sentence_1, sentence_2, sentence_3], None)
        self.assertEqual("O:GRD|B:G-X,G!D-X,RTG-X,DG-!X", key)

    def test_create_key_with_recent_health(self):
        self.decision_making_system = QLearningDecisionMakingSystem([True, -10, 10, 1, 0.1, 0.9, 0.9])

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        key =  self.decision_making_system.create_key(observations, [sentence_1, sentence_2, sentence_3], Health.moreThanHalf)
        self.assertEqual("O:GRD|B:G-X,G!D-X,RTG-X,DG-!X|>=50", key)

    def test_make_decision_for_given(self):
        self.decision_making_system = QLearningDecisionMakingSystem([False, -10, 10, 1, 0.1, 0.9, 0])
        self.decision_making_system.q_table = {
            "O:GRD|B:G-X,G!D-X,RTG-X,DG-!X":{
                Action.eat:0.1,
                Action.explore:0.2
            }
        }
        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        action = self.decision_making_system.make_decision(observations, [sentence_1, sentence_2, sentence_3], None)
        self.assertEqual(Action.explore, action)

    

    def test_make_decision_with_empty_q_table_same_following_state(self):
        self.decision_making_system = QLearningDecisionMakingSystem([False, -10, 10, 1, 0.1, 0.9, 0])

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        available_knowledge = [sentence_1, sentence_2, sentence_3]
        
        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        self.decision_making_system.make_decision(observations, available_knowledge, None)
        self.decision_making_system.update_policy(Reward.nontoxic, observations, available_knowledge, None)

        self.assertEqual(1, len(self.decision_making_system.q_table))
        self.assertEqual(1, max(self.decision_making_system.q_table["O:GRD|B:G-X,G!D-X,RTG-X,DG-!X"].items(), key=lambda x: x[1])[1])

    def test_make_decision_with_empty_q_table_same_following_state_one_more(self):
        self.decision_making_system = QLearningDecisionMakingSystem([False, -10, 10, 1, 0.1, 0.9, 0])

        sentence_1 = Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), NightProposition()], Reward.toxic)], 0.9)
        sentence_2 = Sentence([([NextToRock(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 0.2)
        sentence_3 = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 0.1)

        available_knowledge = [sentence_1, sentence_2, sentence_3]
        
        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]

        self.decision_making_system.make_decision(observations, available_knowledge, None)


        next_observations = [Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]
        
        self.decision_making_system.update_policy(Reward.nontoxic, next_observations, available_knowledge, None)

        self.assertEqual(2, len(self.decision_making_system.q_table))
        self.assertEqual(1, max(self.decision_making_system.q_table["O:GRD|B:G-X,G!D-X,RTG-X,DG-!X"].items(), key=lambda x: x[1])[1])
        self.assertEqual(0, max(self.decision_making_system.q_table["O:GD|B:G-X,G!D-X,RTG-X,DG-!X"].items(), key=lambda x: x[1])[1])

    def test_make_decision_with_empty_q_table_without_knowledge(self):
        self.decision_making_system = QLearningDecisionMakingSystem([False, -10, 10, 1, 0.1, 0.9, 0])

        observations = [Sentence([([ColorGreen(), NextToRock(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), NextToRock()], Reward.none)], 0.1),
        Sentence([([ColorGreen(), DayProposition()], Reward.none)], 0.1),
        Sentence([([ColorGreen()], Reward.none)], 0.1)]
        available_knowledge = []

        self.decision_making_system.make_decision(observations, available_knowledge, None)
        self.decision_making_system.update_policy(Reward.none, observations, available_knowledge, None)
        self.assertEqual(1, len(self.decision_making_system.q_table))
        self.assertEqual(0.1, max(self.decision_making_system.q_table["O:GRD|B"].items(), key=lambda x: x[1])[1])
