import sys
import subprocess

for i in range(2):
    print("Start Config7 run: ", str(i))
    subprocess.call([sys.executable, './ALife.py', "Config7", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'FormalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['EVIDENCE',33], 'DecisionMakingSystem_Args':[0.2, 0.5, 'EVIDENCE', 'False', 'False', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'EVIDENCE'],'yml_file':'Config7.yml'}"])
    print("End Config7 run: ", str(i))