from unittest import TestCase
from .long_term_memory import LongTermMemory
from .propositions import *
from .action import *
from .truths.truthtable import *
from ..evolution import *

class CognitiveSystemTest(TestCase):
    def test_communcation(self):
        kwargs = eval("{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'FormalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithActivationSpreading', 'DecisionMakingSystem':'QLearningDecisionMakingSystem','MentalMap':'True','ObservationSystem_Args':[],'BeliefRevisionSystem_Args':['True'], 'WorkingMemorySystem_Args':['EVIDENCE', 10], 'DecisionMakingSystem_Args':[10,10,1,1,0.9,0.1,0.9], 'CommunicationSystem_Args':['True', 50, 'EVIDENCE']}")
        self.agent = CognitiveEnvolver(None, None, 0, **kwargs)
        self.other_agent = CognitiveEnvolver(None, None, 0, **kwargs)

        other_agents_belief_base = [Sentence([([NextToRock(), NextToTreeTrunk(), DayProposition(), ColorGreen()], Reward.toxic)], 1),
         Sentence([([NextToRock(), NextToTreeTrunk(), NightProposition(), ColorGreen()], Reward.nontoxic)], 2)]
        self.other_agent.cognitive_system.long_term_memory.update(other_agents_belief_base)

        self.agent.cognitive_system.communicate(self.agent, self.other_agent)
        self.assertEqual(1, len(self.agent.cognitive_system.long_term_memory.stored_sentences))
