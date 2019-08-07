from unittest import TestCase
from .long_term_memory import LongTermMemory
from .propositions import *
from .action import *
from .truths.truthtable import *
from ..evolution import *

class CognitiveSystemTest(TestCase):

    def test_first_sentence_single_proposition_system(self):

        kwargs = eval("{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'FormalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithActivationSpreading', 'DecisionMakingSystem':'QLearningDecisionMakingSystem','ObservationSystem_Args':[],'BeliefRevisionSystem_Args':['True'], 'WorkingMemorySystem_Args':[], 'DecisionMakingSystem_Args':[]}")
        self.agent = CognitiveEnvolver(None, None, 0, **kwargs)

        # Observation without reward
        self.agent.cognitive_system.act(self.agent, ColorGreen(), [DayProposition(), NextToRock()], Reward.none)
        # Observation with reward
        self.agent.cognitive_system.act(self.agent, ColorGreen(), [DayProposition(), NextToRock()], Reward.toxic)

        # Now observation with reward should be stored in agents belief base
        self.assertEqual(1, len(self.agent.cognitive_system.long_term_memory.stored_sentences))
        self.assertEqual(1, len(self.agent.cognitive_system.long_term_memory.stored_sentences[0].propositions))
        self.assertEqual(1, self.agent.cognitive_system.long_term_memory.stored_sentences[0].evidence)
        self.assertEqual(3, len(self.agent.cognitive_system.long_term_memory.stored_sentences[0].propositions[0][0]))
        # Q Table should have two states, with reward from observation to reward state
        self.assertEqual(2, len(self.agent.cognitive_system.decision_making_system.q_table.keys()))

        # Another observation with reward
        self.agent.cognitive_system.act(self.agent, ColorGreen(), [DayProposition(), NextToRock()], Reward.toxic)
        # Belief base should stay the same, evidence should be increased
        self.assertEqual(1, len(self.agent.cognitive_system.long_term_memory.stored_sentences[0].propositions))
        self.assertEqual(2, self.agent.cognitive_system.long_term_memory.stored_sentences[0].evidence)
        # Q Table should have same size
        self.assertEqual(2, len(self.agent.cognitive_system.decision_making_system.q_table.keys()))

        # Different Observation without reward, belief base should not be adjusted
        self.agent.cognitive_system.act(self.agent, ColorOrange(), [NightProposition(), NextToRock()], Reward.none)

        # Different Observation with reward
        self.agent.cognitive_system.act(self.agent, ColorOrange(), [NightProposition(), NextToRock()], Reward.nontoxic)
        # Belief Base should be adjusted
        self.assertEqual(3, len(self.agent.cognitive_system.long_term_memory.stored_sentences))

        # Another Different Observation with reward
        self.agent.cognitive_system.act(self.agent, ColorGreen(), [NightProposition(), NextToRock()], Reward.nontoxic)

        # Belief Base should be adjusted once again
        self.assertEqual(7, len(self.agent.cognitive_system.long_term_memory.stored_sentences))

    def test_communcation(self):
        kwargs = eval("{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'FormalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithActivationSpreading', 'DecisionMakingSystem':'QLearningDecisionMakingSystem','ObservationSystem_Args':[],'BeliefRevisionSystem_Args':['True'], 'WorkingMemorySystem_Args':[], 'DecisionMakingSystem_Args':[]}")
        self.agent = CognitiveEnvolver(None, None, 0, **kwargs)
        self.other_agent = CognitiveEnvolver(None, None, 0, **kwargs)

        other_agents_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]
        self.other_agent.cognitive_system.long_term_memory.update(other_agents_belief_base)

        self.agent.cognitive_system.communicate(self.agent, self.other_agent)
        self.assertEqual(1, len(self.agent.cognitive_system.long_term_memory.stored_sentences))
