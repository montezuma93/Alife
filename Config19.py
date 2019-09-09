import sys
import subprocess

for i in range(22):
    print("Start Config19 run: ", str(i))
    subprocess.call([sys.executable, './Alife.py', "Config19", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',25], 'DecisionMakingSystem_Args':[0.2, 0.5, 'RANKING', 'False', 'False', 5, 14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'RANKING'],'yml_file':'Config19.yml'}"])
    print("End Config19 run: ", str(i))