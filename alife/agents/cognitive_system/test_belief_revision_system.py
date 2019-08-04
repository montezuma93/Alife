from unittest import TestCase
from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import *
from .propositions import *
from .belief_revision_system import *


class BeliefRevisionTest(TestCase):
    
    ############################## FORMAL BELIEF REVISION ##############################################
       
    
    def test_create_truth_table_for_belief_base_for_or_sentence_without_negator(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic), ([DayProposition(), NextToRock(), ColorOrange()], Reward.nontoxic)], 1),
         Sentence([([DayProposition(), NextToRock(), ColorOrange()], Reward.nontoxic)], 1)]

        created_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)

        self.assertEqual(TruthTable("((((!(((R&D)&G))^X))&(((!(((R&D)&G))^X))|(((((D&R)&O))^X))))&(((((D&R)&O))^X)))"), created_truth_table)
    
    def test_create_truth_table_for_belief_base_for_or_sentence_with_negator(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic), ([NextToRock(), ColorOrange(), NightProposition()], Reward.toxic)], 1),
         Sentence([([NextToRock(), ColorOrange(), NightProposition()], Reward.toxic)], 1)]

        created_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)

        self.assertEqual(TruthTable("((((!(((R&D)&G))^X))&(((!(((R&D)&G))^X))|((!(((R&O)&!D))^X))))&((!(((R&O)&!D))^X)))"), created_truth_table)
    
    def test_create_truth_table_for_belief_base_for_or_sentence_with_negator_and_non_toxic(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic), ([NextToRock(), ColorOrange(), NightProposition()], Reward.nontoxic)], 1),
         Sentence([([NextToRock(), ColorOrange(), NightProposition()], Reward.nontoxic)], 1)]

        created_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)

        self.assertEqual(TruthTable("((((!(((R&D)&G))^X))&(((!(((R&D)&G))^X))|(((((R&O)&!D))^X))))&(((((R&O)&!D))^X)))"), created_truth_table)
    
    def test_calculate_rank_formal_belief_revision_without_closed_world_assumption_large_belief_base(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic), ([NextToRock(), ColorOrange(), NightProposition()], Reward.nontoxic)], 3),
         Sentence([([NextToRock(), ColorOrange(), NightProposition()], Reward.nontoxic)], 1)]

        sentence = Sentence([([NightProposition(), ColorGreen(), NextToRock], Reward.nontoxic)], 1)

        self.assertEqual(3, self.belief_revision_system.calculate_rank(sentence, old_belief_base))

    def test_calculate_rank_formal_belief_revision_without_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.assertEqual(0, self.belief_revision_system.calculate_rank(sentence, old_belief_base))


    def test_calculate_rank_formal_belief_revision_without_closed_world_assumption_and_new_sentence_has_variable_which_is_not_in_belief_base(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        sentence = Sentence([([DayProposition, NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.assertEqual(1, self.belief_revision_system.calculate_rank(sentence, old_belief_base))

    def test_calculate_rank_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_1(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]

        self.assertEqual(1, self.belief_revision_system.calculate_rank(sentence, old_belief_base))
    
    def test_calculate_rank_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_2(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.assertEqual(2, self.belief_revision_system.calculate_rank(sentence, old_belief_base))
    
    def test_formal_belief_revision_revised_by_same_sentence_should_increase_evidence(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        
        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(2, len(revised_belief_base))
        self.assertEqual(3, revised_belief_base[1].evidence)
    
    def test_formal_belief_revision_without_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        
        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(5, len(revised_belief_base))
        self.assertEqual(1, len(revised_belief_base[0].propositions))
        self.assertEqual(2, len(revised_belief_base[1].propositions))
        self.assertEqual(1, len(revised_belief_base[2].propositions))
        self.assertEqual(2, len(revised_belief_base[3].propositions))
        self.assertEqual(1, len(revised_belief_base[4].propositions))

    def test_formal_belief_revision_with_empty_belief_base(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)

        self.assertEqual(1, len(revised_belief_base))

    def test_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_1(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(4, len(revised_belief_base))
        self.assertEqual(2, len(revised_belief_base[0].propositions))
        self.assertEqual(1, len(revised_belief_base[1].propositions))
        self.assertEqual(2, len(revised_belief_base[2].propositions))
        self.assertEqual(1, len(revised_belief_base[3].propositions))
    
    def test_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_2(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(3, len(revised_belief_base))
        self.assertEqual(2, len(revised_belief_base[0].propositions))
        self.assertEqual(2, len(revised_belief_base[1].propositions))
        self.assertEqual(1, len(revised_belief_base[2].propositions))
    
    def test_revise_belief_for_formal_belief_revision_without_closed_world_assumption_with_ors(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        
        # Revise again with an sentence
        another_sentence = Sentence([([DayProposition(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 3)
        another_revised_belief_base = self.belief_revision_system.revise_belief_base([another_sentence], revised_belief_base)

        self.assertEqual(6, len(another_revised_belief_base))
        self.assertEqual(2, len(another_revised_belief_base[0].propositions))
        self.assertEqual(3, len(another_revised_belief_base[1].propositions))
        self.assertEqual(2, len(another_revised_belief_base[2].propositions))
        self.assertEqual(3, len(another_revised_belief_base[3].propositions))
        self.assertEqual(2, len(another_revised_belief_base[4].propositions))
        self.assertEqual(1, len(another_revised_belief_base[5].propositions))


    def test_revise_belief_for_formal_belief_revision_with_closed_world_assumption_with_ors(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)

        # Revise again with an sentence
        another_sentence = Sentence([([DayProposition(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 3)
        another_revised_belief_base = self.belief_revision_system.revise_belief_base([another_sentence], revised_belief_base)

    ############################### PROBABILITY BELIEF REVISION ##############################################

    def test_probability_belief_revision_without_closed_world_assumption_first_new_sentence(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, False])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(1, len(revised_belief_base))
        self.assertEqual(2/3, revised_belief_base[0].evidence)
    

    def test_probability_belief_revision_closed_world_assumption_and_not_uses_occams_razor_first_new_sentence(self):
        self.belief_revision_system = ProbabilityBeliefRevision([True, False])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(1, len(revised_belief_base))
        self.assertEqual(2/3, revised_belief_base[0].evidence)

    def test_probability_belief_revision_closed_world_assumption_and_uses_occams_razor_first_new_sentence(self):
        self.belief_revision_system = ProbabilityBeliefRevision([True, True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(1, len(revised_belief_base))
        self.assertEqual(2/3, revised_belief_base[0].evidence)

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor_first_new_sentence(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(1, len(revised_belief_base))
        self.assertAlmostEqual(0.394, revised_belief_base[0].evidence, 2)
    
    def test_probability_belief_revision_without_closed_world_assumption(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, False])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(3, len(revised_belief_base))
        self.assertEqual(1.5/3.5, revised_belief_base[0].evidence)
        self.assertEqual(1.5/3.5, revised_belief_base[1].evidence)
        self.assertEqual(1.5/3.5, revised_belief_base[2].evidence)

    def test_probability_belief_revision_without_closed_world_assumption_adding_sentence_again(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, False])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(2, len(revised_belief_base))
        self.assertEqual(2/3.5, revised_belief_base[0].evidence)
        self.assertEqual(1.5/3.5, revised_belief_base[1].evidence)
    

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(3, len(revised_belief_base))
        self.assertAlmostEqual(0.405, revised_belief_base[0].evidence, 2)
        self.assertAlmostEqual(0.405, revised_belief_base[1].evidence, 2)
        self.assertAlmostEqual(0.333, revised_belief_base[2].evidence, 2)

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor_adding_sentence_again(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertAlmostEqual(2, len(revised_belief_base))
        self.assertAlmostEqual(0.449, revised_belief_base[0].evidence, 2)
        self.assertAlmostEqual(0.405, revised_belief_base[1].evidence, 2)

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor_adding_sentence_again_multiple_times(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)

        another_sentence = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)],1)

        another_revised_belief_base = self.belief_revision_system.revise_belief_base([another_sentence], revised_belief_base)
        self.assertAlmostEqual(2, len(another_revised_belief_base))
        self.assertAlmostEqual(0.493, another_revised_belief_base[0].evidence, 2)
        self.assertAlmostEqual(0.373, another_revised_belief_base[1].evidence, 2)

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor_multiple_times(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        
        another_sentence = Sentence([([NightProposition(), ColorGreen()], Reward.toxic)], 1)

        another_revised_belief_base = self.belief_revision_system.revise_belief_base([another_sentence], revised_belief_base)

        self.assertEqual(4, len(another_revised_belief_base))
        self.assertAlmostEqual(0.373, another_revised_belief_base[0].evidence, 2)
        self.assertAlmostEqual(0.373, another_revised_belief_base[1].evidence, 2)
        self.assertAlmostEqual(0.306, another_revised_belief_base[2].evidence, 2)
        self.assertAlmostEqual(0.346, another_revised_belief_base[3].evidence, 2)

 ############################### CONDITIONAL BELIEF REVISION ##############################################

    '''
    
    def test_conditional_belief_revision_create_conditionals(self):
        self.belief_revision_system = ConditionalBeliefRevision()

        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        conditionals = self.belief_revision_system.create_conditionals(old_belief_base)
        self.assertEqual(2, len(conditionals))
        self.assertEqual(["R", "D", "G"], conditionals[0].antecedent)
        self.assertEqual("X", conditionals[0].consequence)
        self.assertEqual(["R", "!D", "G"], conditionals[1].antecedent)
        self.assertEqual("!X", conditionals[1].consequence)

    def test_create_possible_worlds(self):
        self.belief_revision_system = ConditionalBeliefRevision()

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        self.belief_revision_system.variables = get_variable_names_for_all_propositions()
        self.belief_revision_system.create_possible_worlds()
        possible_worlds = self.belief_revision_system.possible_worlds

        self.assertEqual(64, len(possible_worlds))
        self.assertEqual([0, 0, 0, 1, 0, 0, 0, 0], possible_worlds[0])


    def test_calculate_verifying_worlds(self):
        self.belief_revision_system = ConditionalBeliefRevision()

        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.belief_revision_system.variables = get_variable_names_for_all_propositions()
        self.belief_revision_system.create_possible_worlds()
        conditionals = self.belief_revision_system.create_conditionals(old_belief_base)

        verifying_worlds = self.belief_revision_system.calculate_verifying_worlds(conditionals[0])
        self.assertEqual(2, len(verifying_worlds))
        self.assertEqual([1,0,0,0,1,0,1,1], verifying_worlds[0])
        self.assertEqual([1,0,0,0,1,1,1,1], verifying_worlds[1])


    def test_calculate_falsifying_worlds(self):
        self.belief_revision_system = ConditionalBeliefRevision()

        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.belief_revision_system.variables = get_variable_names_for_all_propositions()
        self.belief_revision_system.create_possible_worlds()
        conditionals = self.belief_revision_system.create_conditionals(old_belief_base)

        falsifying_worlds = self.belief_revision_system.calculate_falsifying_worlds(conditionals[0])
        self.assertEqual(2, len(falsifying_worlds))
        self.assertEqual([1,0,0,0,1,0,1,0], falsifying_worlds[0])
        self.assertEqual([1,0,0,0,1,1,1,0], falsifying_worlds[1])

    def test_calculate_list_of_sums_for_k_i_and_falsifying_worlds(self):
        self.belief_revision_system = ConditionalBeliefRevision()

        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.belief_revision_system.variables = get_variable_names_for_all_propositions()
        self.belief_revision_system.create_possible_worlds()
        conditionals = self.belief_revision_system.create_conditionals(old_belief_base)

        falsifying_worlds = self.belief_revision_system.calculate_falsifying_worlds(conditionals[0])
        # Calculate all k_j for index i for falsifyied worlds
        list_of_sums_k_0 = self.belief_revision_system.calculate_list_of_sums(0, conditionals, falsifying_worlds)
        list_of_sums_k_1 = self.belief_revision_system.calculate_list_of_sums(1, conditionals, falsifying_worlds)


    def test_calculate_list_of_sums_for_k_i_and_verified_worlds(self):
        self.belief_revision_system = ConditionalBeliefRevision()

        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.belief_revision_system.variables = get_variable_names_for_all_propositions()
        self.belief_revision_system.create_possible_worlds()
        conditionals = self.belief_revision_system.create_conditionals(old_belief_base)

        verified_worlds = self.belief_revision_system.calculate_verifying_worlds(conditionals[0])
        # Calculate all k_j for index i for falsifyied worlds
        list_of_sums_k_0 = self.belief_revision_system.calculate_list_of_sums(0, conditionals, verified_worlds)
        list_of_sums_k_1 = self.belief_revision_system.calculate_list_of_sums(1, conditionals, verified_worlds)

    def test_create_constraints(self):
        self.belief_revision_system = ConditionalBeliefRevision()

        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        constraints = self.belief_revision_system.calculate_kappa_values(old_belief_base)
    '''