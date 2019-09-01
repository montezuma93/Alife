from unittest import TestCase
from .long_term_memory import LongTermMemory
from .observation_to_proposition_system import *
from .propositions import *
from .belief_revision_system import *


class BeliefRevisionTest(TestCase):
    
    ############################## FORMAL BELIEF REVISION ##############################################

    def test_creation_of_single_sentence_in_belief_base_truth_table(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        belief_base = [Sentence([([ColorGreen()], Reward.toxic)], 1)]

        created_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)
        self.assertEqual(TruthTable("((!(G))|X)"), created_truth_table)


    def test_creation_of_single_sentence_in_belief_base_truth_table_with_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        belief_base = [Sentence([([ColorGreen()], Reward.toxic)], 1)]

        created_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)
        self.assertEqual(TruthTable("((!((((G&!R)&!T)&!D)))|X)"), created_truth_table)

    def test_creation_of_truth_table(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        belief_base = [Sentence([([ColorGreen()], Reward.toxic)], 1),
         Sentence([([ColorGreen(), DayProposition()], Reward.nontoxic)], 1),
         Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), DayProposition()], Reward.nontoxic)], 1),]

        created_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)
        self.assertEqual(TruthTable("((((!(G))|X)&((!((G&D)))|!X))&(((!(G))|X)|((!((G&D)))|!X)))"), created_truth_table)

    def test_more_complexe_creation_of_truth_table(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        belief_base = [Sentence([([ColorGreen()], Reward.toxic)], 1),
         Sentence([([ColorGreen(), DayProposition(), NextToRock()], Reward.nontoxic)], 1),
         Sentence([([ColorGreen()], Reward.toxic), ([ColorGreen(), DayProposition(), NextToRock()], Reward.nontoxic)], 1),]

        created_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)
        self.assertEqual(TruthTable("((((!(G))|X)&((!(((G&D)&R)))|!X))&(((!(G))|X)|((!(((G&D)&R)))|!X)))"), created_truth_table)

    def test_creation_of_new_sentence_truth_table(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        new_sentence = Sentence([([ColorGreen(), DayProposition()], Reward.nontoxic)], 1)

        created_truth_table = self.belief_revision_system.create_truth_table_for_new_sentence(new_sentence)
        self.assertEqual(TruthTable("(((G&D))&(X))"), created_truth_table)

    
    def test_creation_of_new_sentence_truth_table_with_positive_reward(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        new_sentence = Sentence([([ColorGreen(), DayProposition()], Reward.toxic)], 1)

        created_truth_table = self.belief_revision_system.create_truth_table_for_new_sentence(new_sentence)
        self.assertEqual(TruthTable("(((G&D))&(!X))"), created_truth_table)

    def test_creation_of_new_sentence_truth_table_with_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        new_sentence = Sentence([([ColorGreen(), DayProposition()], Reward.nontoxic)], 1)

        created_truth_table = self.belief_revision_system.create_truth_table_for_new_sentence(new_sentence)
        self.assertEqual(TruthTable("(((((G&D)&!R)&!T))&(X))"), created_truth_table)



    def test_does_entail_phi(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        belief_base = [Sentence([([ColorGreen()], Reward.toxic)], 1)]
        belief_base_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)
        new_sentence = Sentence([([ColorGreen(), DayProposition()], Reward.nontoxic)], 1)
        new_sentence_truth_table = self.belief_revision_system.create_truth_table_for_new_sentence(new_sentence)
         
        does_entail_phi = self.belief_revision_system.belief_base_infers_sentence(belief_base_truth_table, new_sentence_truth_table)
        self.assertFalse(does_entail_phi)

    def test_does_entail_phi_with_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        belief_base = [Sentence([([ColorGreen()], Reward.toxic)], 1)]
        belief_base_truth_table = self.belief_revision_system.create_truth_table_for_belief_base(belief_base)
        new_sentence = Sentence([([ColorGreen(), DayProposition()], Reward.nontoxic)], 1)
        new_sentence_truth_table = self.belief_revision_system.create_truth_table_for_new_sentence(new_sentence)
         
        does_entail_phi = self.belief_revision_system.belief_base_infers_sentence(belief_base_truth_table, new_sentence_truth_table)
        self.assertFalse(does_entail_phi)
 
############################################# OLD TESTS ##########################################


    def test_multiple_propositions_observation_works_without_error(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        belief_base = [Sentence([([NextToTreeTrunk, ColorGreen()], Reward.nontoxic)], 1)]
        observation = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.1),
         Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([DayProposition(), NextToRock(), ColorOrange()], Reward.nontoxic)], 1)]
        self.belief_revision_system.revise_belief_base(observation, belief_base)
    
    def test_calculate_rank_formal_belief_revision_without_closed_world_assumption_large_belief_base(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic), ([NextToRock(), ColorOrange(), NightProposition()], Reward.nontoxic)], 3),
         Sentence([([NextToRock(), ColorOrange(), NightProposition()], Reward.nontoxic)], 1)]

        sentence = Sentence([([NightProposition(), ColorGreen(), NextToRock], Reward.nontoxic)], 1)

        self.assertEqual(0, self.belief_revision_system.calculate_rank(sentence, old_belief_base))

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

        self.assertEqual(0, self.belief_revision_system.calculate_rank(sentence, old_belief_base))

    def test_calculate_rank_formal_belief_revision_with_closed_world_assumption_and_b_m_should_be_equal_to_1(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]

        self.assertEqual(0, self.belief_revision_system.calculate_rank(sentence, old_belief_base))

    def test_calculate_rank_formal_belief_revision_with_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        self.assertEqual(0, self.belief_revision_system.calculate_rank(sentence, old_belief_base))
    
    def test_formal_belief_revision_revised_by_same_sentence_should_increase_evidence(self):
        self.belief_revision_system = FormalBeliefRevision([False])
        
        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([DayProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(2, len(revised_belief_base))
        self.assertEqual(2, revised_belief_base[1].evidence)
    
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

    def test_formal_belief_revision_with_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(5, len(revised_belief_base))
        self.assertEqual(1, len(revised_belief_base[0].propositions))
        self.assertEqual(2, len(revised_belief_base[1].propositions))
        self.assertEqual(1, len(revised_belief_base[2].propositions))
        self.assertEqual(2, len(revised_belief_base[3].propositions))
        self.assertEqual(1, len(revised_belief_base[4].propositions))

    def test_another_formal_belief_revision_with_closed_world_assumption(self):
        self.belief_revision_system = FormalBeliefRevision([True])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 2),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(5, len(revised_belief_base))
        self.assertEqual(1, len(revised_belief_base[0].propositions))
        self.assertEqual(2, len(revised_belief_base[1].propositions))
        self.assertEqual(1, len(revised_belief_base[2].propositions))        
        self.assertEqual(2, len(revised_belief_base[3].propositions))
        self.assertEqual(1, len(revised_belief_base[4].propositions))

    def test_revise_belief_for_formal_belief_revision_without_closed_world_assumption_with_ors(self):
        self.belief_revision_system = FormalBeliefRevision([False])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 2)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 1)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        
        # Revise again with an sentence
        another_sentence = Sentence([([DayProposition(), NextToTreeTrunk(), ColorGreen()], Reward.toxic)], 3)
        another_revised_belief_base = self.belief_revision_system.revise_belief_base([another_sentence], revised_belief_base)

        self.assertEqual(11, len(another_revised_belief_base))


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
        self.belief_revision_system = ProbabilityBeliefRevision([False, False, 10])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(1, len(revised_belief_base))
        self.assertEqual(2/3, revised_belief_base[0].evidence)
    

    def test_probability_belief_revision_closed_world_assumption_and_not_uses_occams_razor_first_new_sentence(self):
        self.belief_revision_system = ProbabilityBeliefRevision([True, False, 10])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(1, len(revised_belief_base))
        self.assertEqual(2/3, revised_belief_base[0].evidence)

    def test_probability_belief_revision_closed_world_assumption_and_uses_occams_razor_first_new_sentence(self):
        self.belief_revision_system = ProbabilityBeliefRevision([True, True, 10])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(1, len(revised_belief_base))
        self.assertEqual(2/3, revised_belief_base[0].evidence)

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor_first_new_sentence(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True, 10])

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 1)
        old_belief_base = []

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(1, len(revised_belief_base))
        self.assertAlmostEqual(0.318, revised_belief_base[0].evidence, 2)
    
    def test_probability_belief_revision_without_closed_world_assumption(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, False, 10])

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
        self.belief_revision_system = ProbabilityBeliefRevision([False, False, 10])

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
        self.belief_revision_system = ProbabilityBeliefRevision([False, True, 10])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertEqual(3, len(revised_belief_base))
        self.assertAlmostEqual(0.188, revised_belief_base[0].evidence, 2)
        self.assertAlmostEqual(0.188, revised_belief_base[1].evidence, 2)
        self.assertAlmostEqual(0.26, revised_belief_base[2].evidence, 2)

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor_adding_sentence_again(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True, 10])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        self.assertAlmostEqual(2, len(revised_belief_base))
        self.assertAlmostEqual(0.231, revised_belief_base[0].evidence, 2)
        self.assertAlmostEqual(0.188, revised_belief_base[1].evidence, 2)

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor_adding_sentence_again_multiple_times(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True, 10])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)

        another_sentence = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)],1)

        another_revised_belief_base = self.belief_revision_system.revise_belief_base([another_sentence], revised_belief_base)
        self.assertAlmostEqual(2, len(another_revised_belief_base))
        self.assertAlmostEqual(0.293, another_revised_belief_base[0].evidence, 2)
        self.assertAlmostEqual(0.173, another_revised_belief_base[1].evidence, 2)

    def test_probability_belief_revision_without_closed_world_assumption_and_uses_occams_razor_multiple_times(self):
        self.belief_revision_system = ProbabilityBeliefRevision([False, True, 10])

        self.belief_revision_system.observed_data['RDGX'] = 0.5
        self.belief_revision_system.observed_data['R!DG!X'] = 0.5

        sentence = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 0.5)
        old_belief_base = [Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.5),
         Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.5)]

        revised_belief_base = self.belief_revision_system.revise_belief_base([sentence], old_belief_base)
        
        another_sentence = Sentence([([NightProposition(), ColorGreen()], Reward.toxic)], 1)

        another_revised_belief_base = self.belief_revision_system.revise_belief_base([another_sentence], revised_belief_base)

        self.assertEqual(4, len(another_revised_belief_base))
        self.assertAlmostEqual(0.173, another_revised_belief_base[0].evidence, 2)
        self.assertAlmostEqual(0.173, another_revised_belief_base[1].evidence, 2)
        self.assertAlmostEqual(0.24, another_revised_belief_base[2].evidence, 2)
        self.assertAlmostEqual(0.28, another_revised_belief_base[3].evidence, 2)

 ############################### CONDITIONAL BELIEF REVISION ##############################################

    def test_create_possible_worlds_while_init(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])
        self.assertEqual(4, len(self.belief_revision_system.possible_worlds))
        self.assertEqual(24, len(self.belief_revision_system.possible_worlds["G"]))
        
    

    def test_conditional_belief_revision_create_conditionals(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])

        new_sentence = Sentence([([ColorGreen()], Reward.toxic)], 1)
        kappa_values = self.belief_revision_system.calculate_kappa_values(new_sentence)
        self.assertEqual(0, kappa_values[0][0][1])
        self.assertEqual(0, kappa_values[0][1][1])
        self.assertEqual(0, kappa_values[0][2][1])

    def test_conditional_belief_revision_create_conditionals(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])

        new_sentence = Sentence([([NextToRock(), ColorGreen(), DayProposition()], Reward.nontoxic)], 1)
        kappa_values = self.belief_revision_system.calculate_kappa_values(new_sentence)
        self.assertEqual(0, kappa_values[0][0][1])
        self.assertEqual(0, kappa_values[0][1][1])
        self.assertEqual(0, kappa_values[0][2][1])
    
    def test_conditional_belief_revision_create_conditionals(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])

        new_sentence = Sentence([([NextToRock(), ColorGreen()], Reward.nontoxic)], 1)

        kappa_values = self.belief_revision_system.calculate_kappa_values(new_sentence)
        self.assertEqual(0, kappa_values[0][0][1])
        self.assertEqual(0, kappa_values[0][1][1])
        self.assertEqual(0, kappa_values[0][2][1])

    def test_conditional_belief_revision_create_conditionals_including_negation(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])

        new_sentence = Sentence([([NextToRock(), ColorGreen(), NightProposition()], Reward.nontoxic)], 1)

        kappa_values = self.belief_revision_system.calculate_kappa_values(new_sentence)
        self.assertEqual(0, kappa_values[0][0][1])
        self.assertEqual(0, kappa_values[0][1][1])
        self.assertEqual(0, kappa_values[0][2][1])
        
    def test_conditional_belief_revision_create_conditionals_with_closed_world_assumption(self):
        self.belief_revision_system = ConditionalBeliefRevision([True])

        new_sentence = Sentence([([NextToRock(), ColorGreen(), NightProposition()], Reward.nontoxic)], 1)

        kappa_values = self.belief_revision_system.calculate_kappa_values(new_sentence)
        self.assertEqual(0, kappa_values[0][0][1])
        self.assertEqual(0, kappa_values[0][1][1])
        self.assertEqual(0, kappa_values[0][2][1])
            
    def test_inequalities_solver_in_beginning(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])
        self.assertEqual((1, -1),self.belief_revision_system.solve_gamma_values(0, 0))

    def test_inequalities_solver_anothter(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])
        self.assertEqual((1, -1), self.belief_revision_system.solve_gamma_values(0,2))

    def test_inequalities_solver_one_more(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])
        self.assertEqual((2, -2), self.belief_revision_system.solve_gamma_values(3,1))


    def test_first_sentence_revision(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])

        new_sentences = [Sentence([([ColorGreen()], Reward.toxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)
        

        new_sentences = [Sentence([([ColorGreen(), NightProposition()], Reward.nontoxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)
    
    def test_first_sentence_revision_negative_day(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])    

        new_sentences = [Sentence([([ColorGreen()], Reward.nontoxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)

    
    def test_first_sentence_revision_negative_day(self):
        self.belief_revision_system = ConditionalBeliefRevision([True])    

        new_sentences = [Sentence([([ColorGreen()], Reward.nontoxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)

    def test_first_sentence_revision_negative_day(self):
        self.belief_revision_system = ConditionalBeliefRevision([True])    

        new_sentences = [Sentence([([ColorGreen()], Reward.nontoxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)

    def test_first_sentence_revision(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])

        new_sentences = [Sentence([([ColorGreen()], Reward.toxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)
        

        new_sentences = [Sentence([([ColorGreen(), DayProposition()], Reward.toxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)
    
    def test_first_sentence_revision_second_sentence_is_not_toxic(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])

        new_sentences = [Sentence([([ColorGreen()], Reward.toxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)
        

        new_sentences = [Sentence([([ColorGreen(), DayProposition()], Reward.nontoxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)
    

    def test_first_sentence_revision_with_closed_world_assumption(self):
        self.belief_revision_system = ConditionalBeliefRevision([False])

        new_sentences = [Sentence([([ColorGreen()], Reward.toxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)
        

        new_sentences = [Sentence([([ColorGreen(), DayProposition()], Reward.nontoxic)], 1)]

        self.belief_revision_system.revise_belief_base(new_sentences)
