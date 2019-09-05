import sys
import subprocess

for i in range(10):
    print("Start Config3 run: ", str(i))
    subprocess.call([sys.executable, './Alife.py', "Config3", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'True','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',100], 'DecisionMakingSystem_Args':[0.01, 0.9, 'RANKING', 'True', 'True', 5, 14,14, 15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'RANKING'],'yml_file':'Config3.yml'}"])
    print("End Config3 run: ", str(i))