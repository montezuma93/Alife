import sys
import subprocess

for i in range(42):
    print("Start Config35 run: ", str(i))
    subprocess.call([sys.executable, './Alife.py', "Config35", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ProbabilityBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False','False'], 'WorkingMemorySystem_Args':['PROBABILITY',50], 'DecisionMakingSystem_Args':[0.2, 0.5, 'PROBABILITY', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'PROBABILITY'],'yml_file':'Config35.yml'}"])
    print("End Config35 run: ", str(i))