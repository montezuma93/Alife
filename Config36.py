import sys
import subprocess

procs = []
for i in range(2):
    proc = subprocess.Popen([sys.executable, './Alife.py', "Config36-"+str(i), "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'False','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',50], 'DecisionMakingSystem_Args':[0.2, 0.5, 'RANKING', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'RANKING'],'yml_file':'Config36.yml'}"], close_fds=True)
    procs.append(proc)

for proc in procs:
    proc.wait()