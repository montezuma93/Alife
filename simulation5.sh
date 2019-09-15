#!/bin/bash
#SBATCH -p test_cpu-ivy
#SBATCH --mem=2G
#SBATCH -a 1-1000

python3 "./ALife.py" "Config42-$SLURM_ARRAY_TASK_ID" "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ProbabilityBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'True','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False','False'], 'WorkingMemorySystem_Args':['PROBABILITY',100], 'DecisionMakingSystem_Args':[0.1, 0.5, 'PROBABILITY', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'PROBABILITY'],'yml_file':'Config42.yml'}"
python3 "./ALife.py" "Config43-$SLURM_ARRAY_TASK_ID" "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'True','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',100], 'DecisionMakingSystem_Args':[0.1, 0.5, 'RANKING', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'RANKING'],'yml_file':'Config43.yml'}"
python3 "./ALife.py" "Config45-$SLURM_ARRAY_TASK_ID" "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ProbabilityBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'True','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False','False'], 'WorkingMemorySystem_Args':['PROBABILITY',50], 'DecisionMakingSystem_Args':[0.1, 0.5, 'PROBABILITY', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'PROBABILITY'],'yml_file':'Config45.yml'}"
python3 "./ALife.py" "Config46-$SLURM_ARRAY_TASK_ID" "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'True','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',50], 'DecisionMakingSystem_Args':[0.1, 0.5, 'RANKING', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'RANKING'],'yml_file':'Config46.yml'}"
python3 "./ALife.py" "Config48-$SLURM_ARRAY_TASK_ID" "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ProbabilityBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'True','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False','False'], 'WorkingMemorySystem_Args':['PROBABILITY',25], 'DecisionMakingSystem_Args':[0.1, 0.5, 'PROBABILITY', 'False', 'True', 5,  14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'PROBABILITY'],'yml_file':'Config48.yml'}"
python3 "./ALife.py" "Config49-$SLURM_ARRAY_TASK_ID" "alife.agents.evolution/CognitiveEnvolver/{'ObservationSystem':'MultiplePropositionSystem','BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence','DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'True','ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',25], 'DecisionMakingSystem_Args':[0.1, 0.5, 'RANKING', 'False', 'True', 5, 14,14,15,7, 7, 7, 7],'CommunicationSystem_Args':['False', 10, 'RANKING'],'yml_file':'Config49.yml'}"