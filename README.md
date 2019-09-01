ALife
=======================

This is my master thesis project.
The original code was not done by me.
It was taken from https://github.com/jmread/alife.

The goal of this project is to extend the given world of bugs and create and compare different cognitive models for inductive reasoning for the living bugs.

The extensions of the world are:
	- Add the possibily to create the world randomized.
	- Add day and night.
	- Add different objects (rocks, tree-trunk).
	- Add multiple kind of plants (toxic, non-toxic) -> Toxicity can depend on closed by objects and day time
	- Add communicating system between the bugs.

In conf.yml the cognitive system of an agent can be determined:
	-> Define it as CognitiveEnvolver (alife.agents.evolution/CognitiveEnvolver/)
	-> Add key-value object for defining which cognitive modules and params to use for the cognitive system of the agent:

	Example:
		{'ObservationSystem':'OccamsRazorMultiplePropositionSystem',
		'BeliefRevisionSystem':'ConditionalBeliefRevision', 'WorkingMemorySystem':'WorkingMemoryWithEvidence',
		'DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem', 'MentalMap':'True',
		'ObservationSystem_Args':[], 'BeliefRevisionSystem_Args':['False'], 'WorkingMemorySystem_Args':['RANKING',
		10], 'DecisionMakingSystem_Args':[0.1, 0.9, 'RANKING', 'True', 'True', 5, 20,
		21, 22, 25, 7, 6, 5], 'CommunicationSystem_Args':['True', 10, 'RANKING']}
	
	Possible Values for the specific Keys:
	'ObservationSystem': 'MultiplePropositionSystem'; 'OccamsRazorMultiplePropositionSystem'; 'SinglePropositionSystem'; 'RandomSinglePropositionSystem'
	'ObservationSystem_Args': []

	'BeliefRevisionSystem': 'ConditionalBeliefRevision'; 'FormalBeliefRevision'; 'ProbabilityBeliefRevision'
	'BeliefRevisionSystem_Args':[ClosedWorldAssumption('True'/'False'), UseOccamsRazorPrinziple('True'/'False')(Just for ProbabilityBeliefRevision),
	 PseudoSampleSize(int) (Just for ProbabilityBeliefRevision)]

	'WorkingMemorySystem': 'WorkingMemoryWithEvidence'; 'WorkingMemoryWithActivationSpreading';
	'WorkingMemorySystem_Args':[EvidenceInterpreation('RANKING','EVIDENCE','PROBABILITY'), 
	 PercentageAmountForRetrieving(0-100)/PercentageAmountIncludingEvidenceValue(0-100)]

	'DecisionMakingSystem':'HumanLikeDecisionMakingUnderUncertaintySystem'; 'QLearningDecisionMakingSystem'
	'DecisionMakingSystem_Args'(For HumanLikeDecisionMakingUnderUncertaintySystem): [RiskAversion(float 0-1), AmbiguityAversion(float 0-1), 
	 EvidenceInterpretation('RANKING','EVIDENCE','PROBABILITY'), ClosedWorldAssumption('True'/'False'), UseRecentHealth('True'/'False'),
	 If UseRecentHealth: RewardEat->75(int >0), RewardEat->=50(int>0), RewardEat-<50(int>0),RewardEat-<25(int>0), 
	 RewardExplore->75(int>0), RewardExplore->=50(int>0), RewardExplore-<50(int>0), RewardExplore-<25(int>0)
	 Else: RewardEat(int>0), RewardExplore(int>0)]
	
	'DecisionMakingSystem_Args'(For QLearningDecisionMakingSystem): [UseRecentHealth('True'/'False'), 
	 RewardEatToxic(int), RewardEatNonToxic(int), RewardExplore(int), LearningRate(float 0-1), DiscountFactor(float 0-1),
	 ExplorationProbability(float 0-1)]
	
	'MentalMap':('True'/'False') 

	'CommunicationSystem_Args': [UseCommunication('True'/'False'), TopPercentageAmountOfSentencesShared(0-100), 
	 EvidenceInterpreation('RANKING','EVIDENCE','PROBABILITY')]
