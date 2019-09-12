import sys
import subprocess

procs = []
for i in range(2):
    proc = subprocess.Popen([sys.executable, './ALife.py', "Config1-"+str(i), "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'FormalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['EVIDENCE',100], 'DecisionMakingSystem_Args':[0.01, 0.9, 'EVIDENCE', 'False', 'False', 5, 14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'EVIDENCE'],'yml_file':'Config1.yml'}"], close_fds=True)
    procs.append(proc)

for proc in procs:
    proc.wait()