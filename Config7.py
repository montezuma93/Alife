import sys
import subprocess

procs = []
for i in range(12):
    proc = subprocess.Popen([sys.executable, './ALife.py', "Config7-"+str(i), "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'FormalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['EVIDENCE',33], 'DecisionMakingSystem_Args':[0.2, 0.5, 'EVIDENCE', 'False', 'False', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'EVIDENCE'],'yml_file':'Config7.yml'}"], close_fds=True)
    procs.append(proc)

for proc in procs:
    proc.wait()