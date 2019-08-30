from alife.agents.agent import Agent
from numpy import zeros, dot, clip, zeros, tanh, dot, unique
from numpy.random import rand, randn, choice
from alife.agents.models import SLP, MLP, ESN
import numpy as np
from .cognitive_system.cognitive_system import Cognitive_System
from .cognitive_system.propositions import *



class SimpleEvolver(Agent):
    '''
        A simple agent based on some (specified) kind of neural network.

        Initially a random weight matrix, and thenceforth a random mutation 
        ('copy') of a parent agent, an evolution strategy is handled implicitly 
        by the environment: poor quality agents will simply not survive long 
        enough to be able to copy themselves; and thus are extinguished. 

        Thus, this agent relies entirely on generation-to-generation evolution 
        to make any progress.
    '''

    def __init__(self, obs_space, act_space, H=0, **kwargs):
        """
            Init.

            Parameters
            ----------

            obs_space : BugSpace
                observation space
            act_space : BugSpace
                action space
            H : int
                number of hidden units (negative for recurrent)

        """
        self.obs_space = obs_space
        self.act_space = act_space

        D = obs_space.shape[0]
        L = act_space.shape[0]

        if 'H' in kwargs:
            H = kwargs['H']

        if H > 0:
            self.h = MLP(D,L,H)
        elif H < 0:
            self.h = ESN(D,L,-H)
        else:
            self.h = SLP(D,L)

        # Uniq ID (for visualization)
        self.id_num = str(choice(1000))+':'
        self.generation = 1

    def act(self,obs,reward,done=False):
        """
            Act.

            Parameters
            ----------

            obs : numpy array of length D
                the state at the current time
            reward : float
                the reward signal at the current time

            Returns
            -------

            A number array of length L 
                (the action to take)
        """
        return self.h.predict(obs)

    def copy(self):
        """
            Copy.
            
            A new copy (child) of this agent, [optionally] based on this one (the parent).
        """

        new = SimpleEvolver(self.obs_space,self.act_space)
        new.generation = self.generation+1
        new.id_num = self.id_num + str(choice(10))
        new.h = self.h.copy(modify=True)

        return new

    def __str__(self):
        ''' Return a string representation (e.g., a label) for this agent '''
        return ("%s\nID:%s\nGen.%d" % (str(self.h.__class__.__name__), self.id_num,self.generation))

#    def load(self, file_name):
#        self.generation = 0 # TODO extract from filename
#        self.h = None # TODO unpickle

    def save(self, bin_path, log_path):
        # TODO pickle self.h to ~/bin_path/:module:self.__class__.__name__:self.generation.dat
        print("Save: Not yet implemented!")
        return



class CognitiveEnvolver(Agent):
    '''
        A simple agent based on some (specified) kind of neural network.

        Initially a random weight matrix, and thenceforth a random mutation 
        ('copy') of a parent agent, an evolution strategy is handled implicitly 
        by the environment: poor quality agents will simply not survive long 
        enough to be able to copy themselves; and thus are extinguished. 

        Thus, this agent relies entirely on generation-to-generation evolution 
        to make any progress.
    '''

    def __init__(self, obs_space=None, act_space=None, H=0, **kwargs):
        # Uniq ID (for visualization)
        self.id_num = str(choice(1000))+':'
        self.generation = 1

        #Create cognitive system
        self.cognitive_system = Cognitive_System(kwargs.get("ObservationSystem"), kwargs.get("BeliefRevisionSystem"),
         kwargs.get("WorkingMemorySystem"), kwargs.get("DecisionMakingSystem"), kwargs.get("MentalMap"),
          kwargs.get("ObservationSystem_Args"), kwargs.get("BeliefRevisionSystem_Args"), kwargs.get("WorkingMemorySystem_Args"),
           kwargs.get("DecisionMakingSystem_Args"), kwargs.get("CommunicationSystem_Args"))
        

    def act(self, obs, nearby_objects, is_day_time, reward, world, pos, currentHealth, done=False):
        """
            Act.

            Parameters
            ----------

            obs : numpy array of length D
                the state at the current time
            reward : float
                the reward signal at the current time

            Returns
            -------

            A number array of length L 
                (the action to take)
        """
        # Merge nearby objects
        merged_nearby_objects = list(set().union(nearby_objects[0], nearby_objects[1],nearby_objects[2]))
        # Create prposition
        actual_reward = self._cast_to_reward(reward)
        propositions = self._cast_to_proposition(merged_nearby_objects, is_day_time)
        action = self.cognitive_system.act(self, propositions[0], propositions[1], actual_reward, world, pos, currentHealth)
        return action

    def communicate(self, other_agent):
        if self.cognitive_system.communication_system.able_to_communicate:
            self.cognitive_system.communicate(self, other_agent.brain)

    def _cast_to_reward(self, reward):
        if reward > 0:
            return Reward.nontoxic
        elif reward <= -10:
            return Reward.toxic
        else:
            return Reward.none

    def _cast_to_proposition(self,nearby_objects, is_day_time):
        propositions = []
        color_proposition = None
        id_to_proposition_mapping = {
            1: NextToRock(),
            2: NextToTreeTrunk(),
            3: ColorGreen(),
            31: ColorOrange(),
            32: ColorPurple(),
            33: ColorBlue()
        }
        for near_object_id in nearby_objects:
            if near_object_id == 1  or near_object_id == 2:
                propositions.append(id_to_proposition_mapping.get(near_object_id))
            else:
                color_proposition = id_to_proposition_mapping.get(near_object_id)
        propositions.append(self._cast_to_day_time_proposition(is_day_time))
        return (color_proposition, propositions)

    def _cast_to_day_time_proposition(self, is_day_time):
        if is_day_time:
            return DayProposition()
        else:
            return NightProposition()

    
    def copy(self):
        """
            Copy.
            
            A new copy (child) of this agent, [optionally] based on this one (the parent).
        """

        new = SimpleEvolver(self.obs_space,self.act_space)
        new.generation = self.generation+1
        new.id_num = self.id_num + str(choice(10))
        new.h = self.h.copy(modify=True)

        return new

    def __str__(self):
        ''' Return a string representation (e.g., a label) for this agent '''
        return ("ID:%s\nGen.%d" % (self.id_num,self.generation))

#    def load(self, file_name):
#        self.generation = 0 # TODO extract from filename
#        self.h = None # TODO unpickle

    def save(self, bin_path, log_path):
        # TODO pickle self.h to ~/bin_path/:module:self.__class__.__name__:self.generation.dat
        print("Save: Not yet implemented!")
        return




