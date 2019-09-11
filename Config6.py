import sys
import subprocess

for i in range(42):
    print("Start Config6 run: ", str(i))
    subprocess.call([sys.executable, './Alife.py', "Config6", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',50], 'DecisionMakingSystem_Args':[0.2, 0.5, 'RANKING', 'False', 'False', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'RANKING'],'yml_file':'Config6.yml'}"])
    print("End Config6 run: ", str(i))