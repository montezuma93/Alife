import sys
import subprocess

for i in range(42):
    print("Start Config25 run: ", str(i))
    subprocess.call([sys.executable, './Alife.py', "Config25", "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ProbabilityBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False','False'], 'WorkingMemorySystem_Args':['PROBABILITY',50], 'DecisionMakingSystem_Args':[0.9, 0.5, 'PROBABILITY', 'False', 'False', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'PROBABILITY'],'yml_file':'Config25.yml'}"])
    print("End Config25 run: ", str(i))