import sys
import subprocess

for i in range(42):
    print("Start Config32 run: ", str(i))
    subprocess.call([sys.executable, './Alife.py', "Config32", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ProbabilityBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False','False'], 'WorkingMemorySystem_Args':['PROBABILITY',100], 'DecisionMakingSystem_Args':[0.2, 0.5, 'PROBABILITY', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'PROBABILITY'],'yml_file':'Config32.yml'}"])
    print("End Config32 run: ", str(i))