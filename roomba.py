"""Roomba agents policy generator.
"""

import numpy as np
import random


class PolicyGen:
    """Policy generator class for CtF env.

    This class can be used as a template for policy generator.
    Designed to summon an AI logic for the team of units.

    Methods:
        gen_action: Required method to generate a list of actions.
    """

    def __init__(self, free_map, agent_list):
        """Constuctor for policy class.

        This class can be used as a template for policy generator.

        Args:
            free_map (np.array): 2d map of static environment.
            agent_list (list): list of all friendly units.
        """
        self.random = np.random
        self.free_map = free_map
        # self.heading_right = [True] * len(agent_list) #: Attr to track directions.

    def gen_action(self, agent_list, observation, free_map=None):
        """Action generation method.

        This is a required method that generates list of actions corresponding
        to the list of 1units.

        Args:
            agent_list (list): list of all friendly units.
            observation (np.array): 2d map of partially observable map.
            free_map (np.array): 2d map of static environment (optional).

        Returns:
            action_out (list): list of integers as actions selected for team.
        """
        action_out = []
        # for i in agent_list:
        #     action_out.append(self.random.randint(0, 5)) # choose random action
        #
        # return action_out
        if free_map is not None: self.free_map = free_map

        for idx, agent in enumerate(agent_list):
            a = self.roomba(agent, idx, observation)
            action_out.append(a)

        return action_out

    def roomba(self, agent, idx, obs):
        """
        Policy: find the flag and capture it only using observations
                from the environment.
                can also win by killing all the enemies.
                Recommendation: make a roomba type policy - go in random directions,
                if you see enemy or obstable - turn away.
        """

        x,y = agent.get_loc()
        action = 0
        
        # 0 -> do nothing/stay
        # 1 -> up
        # 2 -> right
        # 3 -> down
        # 4 -> left
        # rand_action = random.choice(0, 5)
        # if obstacle at left then choose any direction except left

        action = self.random.randint(0, 5)
        
        if (x>0 and obs[x-1][y] != self.free_map[x][y]):
            action = int(random.choice([0,1,2,3]))

        elif (x+1 < len(self.free_map) and obs[x+1][y] != self.free_map[x][y]):
            action = int(random.choice([0,1,4,3]))

        elif (y > len(self.free_map) and obs[x][y-1] != self.free_map[x][y]):
            action = int(random.choice([0,2,4,3]))

        elif (y < len(self.free_map) - 1 and obs[x][y+1] != self.free_map[x][y]):
            action = int(random.choice([0,1,4,2]))

        return action
