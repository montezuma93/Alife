from unittest import TestCase
from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import *
from .propositions import *
from .belief_revision_system import *

class BeliefRevisionTest(TestCase):

    ############################### FORMAL BELIEF REVISION ##############################################

    def test_calculate_rank_formal_belief_revision_without_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(False)

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.assertEqual(0, self.belief_revision_system.calculate_rank(sentence, old_belief_base))
   

    def test_calculate_rank_formal_belief_revision_without_closed_world_assumption_and_new_sentence_has_variable_which_is_not_in_belief_base(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(False)

        sentence = Sentence([([DayProposition, NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.assertEqual(1, self.belief_revision_system.calculate_rank(sentence, old_belief_base))

    def test_calculate_rank_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_1(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(True)

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]

        self.assertEqual(1, self.belief_revision_system.calculate_rank(sentence, old_belief_base))
    
    def test_calculate_rank_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_2(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(True)

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.assertEqual(2, self.belief_revision_system.calculate_rank(sentence, old_belief_base))

    def test_formal_belief_revision_without_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(False)

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base(sentence, old_belief_base)
        self.assertEqual(5, len(revised_belief_base))
        self.assertEqual(1, len(revised_belief_base[0].propositions))
        self.assertEqual(2, len(revised_belief_base[1].propositions))
        self.assertEqual(1, len(revised_belief_base[2].propositions))
        self.assertEqual(2, len(revised_belief_base[3].propositions))
        self.assertEqual(1, len(revised_belief_base[4].propositions))

    def test_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_1(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(True)

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]

        revised_belief_base = self.belief_revision_system.revise_belief_base(sentence, old_belief_base)
        self.assertEqual(4, len(revised_belief_base))
        self.assertEqual(2, len(revised_belief_base[0].propositions))
        self.assertEqual(1, len(revised_belief_base[1].propositions))
        self.assertEqual(2, len(revised_belief_base[2].propositions))
        self.assertEqual(1, len(revised_belief_base[3].propositions))
    
    def test_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_2(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(True)

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base(sentence, old_belief_base)
        self.assertEqual(3, len(revised_belief_base))
        self.assertEqual(2, len(revised_belief_base[0].propositions))
        self.assertEqual(2, len(revised_belief_base[1].propositions))
        self.assertEqual(1, len(revised_belief_base[2].propositions))
    
    def test_revise_belief_for_formal_belief_revision_without_closed_world_assumption_with_ors(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(False)

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base(sentence, old_belief_base)
        
        # Revise again with an sentence
        another_sentence = Sentence([([DayProposition(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 3)
        another_revised_belief_base = self.belief_revision_system.revise_belief_base(another_sentence, revised_belief_base)

        self.assertEqual(6, len(another_revised_belief_base))
        self.assertEqual(2, len(another_revised_belief_base[0].propositions))
        self.assertEqual(3, len(another_revised_belief_base[1].propositions))
        self.assertEqual(2, len(another_revised_belief_base[2].propositions))
        self.assertEqual(3, len(another_revised_belief_base[3].propositions))
        self.assertEqual(2, len(another_revised_belief_base[4].propositions))
        self.assertEqual(1, len(another_revised_belief_base[5].propositions))


    def test_revise_belief_for_formal_belief_revision_with_closed_world_assumption_with_ors(self):
        self.belief_revision_system = FormalBeliefRevision()
        self.belief_revision_system.set_closed_world_assumption(True)

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]

        revised_belief_base = self.belief_revision_system.revise_belief_base(sentence, old_belief_base)

        # Revise again with an sentence
        another_sentence = Sentence([([DayProposition(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 3)
        another_revised_belief_base = self.belief_revision_system.revise_belief_base(another_sentence, revised_belief_base)
