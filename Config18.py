import sys
import subprocess

for i in range(22):
    print("Start Config18 run: ", str(i))
    subprocess.call([sys.executable, './Alife.py', "Config18", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'ProbabilityBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False','False'], 'WorkingMemorySystem_Args':['PROBABILITY',25], 'DecisionMakingSystem_Args':[0.2, 0.5, 'PROBABILITY', 'False', 'False', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'PROBABILITY'],'yml_file':'Config18.yml'}"])
    print("End Config18 run: ", str(i))