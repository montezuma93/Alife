import sys
import subprocess

procs = []
for i in range(12):
    proc = subprocess.Popen([sys.executable, './ALife.py', "Config9-"+str(i), "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'SinglePropositionSystem','BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',25], 'DecisionMakingSystem_Args':[0.2, 0.5, 'RANKING','False', 'False', 5, 14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'RANKING'],'yml_file':'Config9.yml'}"], close_fds=True)
    procs.append(proc)

for proc in procs:
    proc.wait()