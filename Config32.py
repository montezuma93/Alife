import sys
import subprocess

procs = []
for i in range(2):
    proc = subprocess.Popen([sys.executable, './Alife.py', "Config32-"+str(i), "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ProbabilityBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False','False'], 'WorkingMemorySystem_Args':['PROBABILITY',100], 'DecisionMakingSystem_Args':[0.2, 0.5, 'PROBABILITY', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'PROBABILITY'],'yml_file':'Config32.yml'}"], close_fds=True)
    procs.append(proc)

for proc in procs:
    proc.wait()