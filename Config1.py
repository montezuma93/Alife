import sys
import subprocess

for i in range(12):
    print("Start Config1 run: ", str(i))
    subprocess.call([sys.executable, './Alife.py', "Config1", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'FormalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['EVIDENCE',100], 'DecisionMakingSystem_Args':[0.01, 0.9, 'EVIDENCE', 'False', 'False', 5, 14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'EVIDENCE'],'yml_file':'Config1.yml'}"])
    print("End Config1 run: ", str(i))