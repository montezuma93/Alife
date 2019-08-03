from unittest import TestCase
from .long_term_memory import LongTermMemory
from .propositions import *
from ..evolution import *

class CognitiveSystemTest(TestCase):
 
    def test_first_sentence(self):
        kwargs = eval("{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'FormalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithActivationSpreading',            'DecisionMakingSystem':'QLearningDecisionMakingSystem','ObservationSystem_Args':[],'BeliefRevisionSystem_Args':['True'], 'WorkingMemorySystem_Args':[], 'DecisionMakingSystem_Args':[]}")
        self.agent = CognitiveEnvolver(None, None, 0, **kwargs)
        self.agent.cognitive_system.act(self.agent, ColorGreen(), [DayProposition(), NextToRock()], Reward.none)
        self.agent.cognitive_system.act(self.agent, ColorGreen(), [DayProposition(), NextToRock()], Reward.toxic)