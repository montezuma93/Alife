from unittest import TestCase
from .long_term_memory import LongTermMemory
from .working_memory import WorkingMemoryWithEvidence, WorkingMemoryWithActivationSpreading, EvidenceInterpretation
from .propositions import *

 
class WorkingMemoryTest(TestCase):
 
########################### WORKING MEMORY ###########################################

    def test_set_percentage(self):
        self.working_memory = WorkingMemoryWithEvidence([EvidenceInterpretation.evidence.value, 100])

        self.working_memory.set_percentage_amount_for_retrieving(0)
        self.assertEqual(100, self.working_memory.percentage_amount_for_retrieving)
        self.working_memory.set_percentage_amount_for_retrieving(101)
        self.assertEqual(100, self.working_memory.percentage_amount_for_retrieving)
        self.working_memory.set_percentage_amount_for_retrieving(50)
        self.assertEqual(50, self.working_memory.percentage_amount_for_retrieving)

    def test_retrieve_sentences_all(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithEvidence([EvidenceInterpretation.evidence.value, 100])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)
        sentence_4 = Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorOrange()], Reward.nontoxic)], 2)
        sentence_5 = Sentence([([NextToRock(), ColorOrange()], Reward.nontoxic)], 1)

        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5]
        available_knowledge = self.working_memory.retrieve_knowledge(None, self.long_term_memory)
        self.assertEqual(5, len(available_knowledge))

    def test_retrieve_sentences_some(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithEvidence([EvidenceInterpretation.evidence.value, 50])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)
        sentence_4 = Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorOrange()], Reward.nontoxic)], 2)
        sentence_5 = Sentence([([NextToRock(), ColorOrange()], Reward.nontoxic)], 1)

        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5]
        available_knowledge = self.working_memory.retrieve_knowledge(None, self.long_term_memory)
        self.assertEqual(4, len(available_knowledge))


    def test_retrieve_sentences_some_including_new_sentence(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithEvidence([EvidenceInterpretation.evidence.value, 10])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)
        sentence_4 = Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorOrange()], Reward.nontoxic)], 2)
        sentence_5 = Sentence([([NextToRock(), ColorOrange()], Reward.nontoxic)], 1)

        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5]

        new_sentence = Sentence([([DayProposition(), ColorOrange()], Reward.none)], 3)

        available_knowledge = self.working_memory.retrieve_knowledge(new_sentence, self.long_term_memory)
        self.assertEqual(2, len(available_knowledge))
 
########################### WORKING MEMORY WITH ACTIVATION SPREADING ###########################################

    def test_calculate_sentences_with_activation_spreading_with_new_sentence(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithActivationSpreading([EvidenceInterpretation.evidence.value, 100])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)
        sentence_4 = Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorOrange()], Reward.nontoxic)], 2)
        sentence_5 = Sentence([([NextToRock(), ColorOrange()], Reward.nontoxic)], 1)
        sentence_6 = Sentence([([NextToTreeTrunk(), ColorOrange()], Reward.nontoxic)], 1)
        new_sentence = Sentence([([ColorBlue(), DayProposition(), NextToRock()], Reward.toxic)], 3)
        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5, sentence_6]

        self.working_memory.init_activation_value_property(self.long_term_memory.stored_sentences)
        self.working_memory.spread_activation([new_sentence], self.long_term_memory.stored_sentences)

        self.assertEqual(0.5, sentence_1.activation_value)
        self.assertEqual(0.75, sentence_2.activation_value)
        self.assertEqual(0.25, sentence_3.activation_value)
        self.assertEqual(0.25, sentence_4.activation_value)
        self.assertEqual(0.25, sentence_5.activation_value)
        self.assertEqual(0, sentence_6.activation_value)

    def test_add_calculated_base_activation_activation_spreading(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithActivationSpreading([EvidenceInterpretation.evidence.value, 100])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_1.usages = [1]
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_2.usages = [2, 4, 5]
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)
        sentence_3.usages = [3]

        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3]

        self.working_memory.init_activation_value_property(self.long_term_memory.stored_sentences)
        self.working_memory.add_calculated_base_activation(self.long_term_memory.stored_sentences, 6)

        self.assertAlmostEqual(-0.80471895621, sentence_1.activation_value)
        self.assertAlmostEqual(0.79168250906, sentence_2.activation_value)
        self.assertAlmostEqual(-0.54930614433, sentence_3.activation_value)

    def test_retrieve_knowledge_with_activation_spreading_with_new_sentence(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithActivationSpreading([EvidenceInterpretation.evidence.value, 50])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_1.usages = [1]
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_2.usages = [2,7]
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)
        sentence_3.usages = [3,8]
        sentence_4 = Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorOrange()], Reward.nontoxic)], 2)
        sentence_4.usages = [4,9]
        sentence_5 = Sentence([([NextToRock(), ColorOrange()], Reward.nontoxic)], 1)
        sentence_5.usages = [5]
        sentence_6 = Sentence([([NextToTreeTrunk(), ColorOrange()], Reward.nontoxic)], 1)
        sentence_6.usages = [6]
        new_sentence = Sentence([([ColorBlue(), DayProposition(), NextToRock()], Reward.toxic)], 3)
        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5, sentence_6]

        self.long_term_memory.set_time_since_initialization(10)
        available_sentences = self.working_memory.retrieve_knowledge([new_sentence], self.long_term_memory)

        self.assertEqual(3, len(available_sentences))


    def test_retrieve_knowledge_with_activation_spreading_with_new_sentence_including_evidence(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithActivationSpreading([EvidenceInterpretation.evidence.value, 75])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_1.usages = [1]
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 3)
        sentence_2.usages = [2,7]
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)
        sentence_3.usages = [3,8]
        sentence_4 = Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorOrange()], Reward.nontoxic)], 2)
        sentence_4.usages = [4,9]
        sentence_5 = Sentence([([NextToRock(), ColorOrange()], Reward.nontoxic)], 1)
        sentence_5.usages = [5]
        sentence_6 = Sentence([([NextToTreeTrunk(), ColorOrange()], Reward.nontoxic)], 1)
        sentence_6.usages = [6]
        new_sentence = Sentence([([ColorBlue(), DayProposition(), NextToRock()], Reward.toxic)], 3)
        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5, sentence_6]

        self.long_term_memory.set_time_since_initialization(10)
        available_sentences = self.working_memory.retrieve_knowledge([new_sentence], self.long_term_memory)

        self.assertEqual(4, len(available_sentences))


    def test_retrieve_knowledge_with_activation_spreading_with_new_sentence_including_probability(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithActivationSpreading([EvidenceInterpretation.probability.value, 10])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 0.1)
        sentence_1.usages = [1]
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 0.1)
        sentence_2.usages = [2,7]
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 0.2)
        sentence_3.usages = [3,8]
        sentence_4 = Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorOrange()], Reward.nontoxic)], 0.3)
        sentence_4.usages = [4,9]
        sentence_5 = Sentence([([NextToRock(), ColorOrange()], Reward.nontoxic)], 0.4)
        sentence_5.usages = [5]
        sentence_6 = Sentence([([NextToTreeTrunk(), ColorOrange()], Reward.nontoxic)], 0.5)
        sentence_6.usages = [6]
        new_sentence = Sentence([([ColorBlue(), DayProposition(), NextToRock()], Reward.toxic)], 0.5)
        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5, sentence_6]

        self.long_term_memory.set_time_since_initialization(10)
        available_sentences = self.working_memory.retrieve_knowledge([new_sentence], self.long_term_memory)

        self.assertEqual(3, len(available_sentences))

    def test_retrieve_knowledge_with_activation_spreading_with_new_sentence_including_ranking(self):
        self.long_term_memory = LongTermMemory()
        self.working_memory = WorkingMemoryWithActivationSpreading([EvidenceInterpretation.ranking.value, 10])

        sentence_1 = Sentence([([DayProposition(), ColorGreen()], Reward.toxic)], 0)
        sentence_2 = Sentence([([NextToRock(), DayProposition(), ColorGreen()], Reward.toxic)], 1)
        sentence_3 = Sentence([([NextToRock(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)
        sentence_4 = Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorOrange()], Reward.nontoxic)], 2)
        sentence_5 = Sentence([([NextToRock(), ColorOrange()], Reward.nontoxic)], 4)
        sentence_6 = Sentence([([NextToTreeTrunk(), ColorOrange()], Reward.nontoxic)], 8)
        new_sentence = Sentence([([ColorBlue(), DayProposition(), NextToRock()], Reward.toxic)], 2)
        self.long_term_memory.stored_sentences = [sentence_1, sentence_2, sentence_3, sentence_4, sentence_5, sentence_6]

        self.long_term_memory.set_time_since_initialization(10)
        available_sentences = self.working_memory.retrieve_knowledge([new_sentence], self.long_term_memory)

        self.assertEqual(4, len(available_sentences))
