"""Roomba agents policy generator.

This module demonstrates an example of a simple heuristic policy generator
for Capture the Flag environment.
    http://github.com/osipychev/missionplanner/

DOs/Denis Osipychev
    http://www.denisos.com
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
        # initialize all the directions with False
        self.heading_right = [False] * len(agent_list) #: Attr to track directions.
        # self.heading_left = [False] * len(agent_list)
        self.heading_up = [False] * len(agent_list)
        # self.heading_down = [False] * len(agent_list)

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
            # First choose a random direction to go into
            starting_action = self.random.randint(0, 5)
            # Initializing the direction based on the starting_action
            if starting_action == 1:
                self.heading_up[idx] = True
            elif starting_action == 2:
                self.heading_right[idx] = True
            # elif starting_action == 3:
            #     self.heading_down[idx] = True
            # elif starting_action == 4:
            #     self.heading_left[idx] = True

            a = self.roomba(agent, idx, observation)

            # if starting_action < 3:
            #     a = self.roomba(agent, idx, observation)
            # else:
            #     a = starting_action
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
        # 1 -> heading_up
        # 2 -> heading_right
        # 3 -> heading_down
        # 4 -> heading_left

        # heading up and down
        # and
        #     self.free_map[x][y-1] == self.free_map[x][y])


        # if (not self.heading_down[idx] and y > 0 and
        #     obs[x][y-1] == self.free_map[x][y]):
        #     action = 1
        # elif (self.heading_down[idx] and y < len(self.free_map[0])-1 and
        #     obs[x][y+1] == self.free_map[x][y]):
        #     action = 3
        # else:
        #     if (not self.heading_down[idx] and y > 0 and
        #         obs[x][y-1] != self.free_map[x][y]):
        #         self.heading_down[idx] = not self.heading_down[idx]
        #         action = 3
        #     elif (self.heading_down[idx] and y < len(self.free_map[0])-1 and
        #         obs[x][y+1] != self.free_map[x][y]):
        #         self.heading_down[idx] = not self.heading_down[idx]
        #         action = 1
        #     else:
        #         self.heading_down[idx] = not self.heading_down[idx]

        if (self.heading_up[idx] and y > 0 and
            obs[x][y-1] == self.free_map[x][y]):
            action = 1
        elif (not self.heading_up[idx] and y < len(self.free_map[0])-1 and
            obs[x][y+1] == self.free_map[x][y]):
            action = 3
        else:
            if (self.heading_up[idx] and y > 0 and
                obs[x][y-1] != self.free_map[x][y]):
                self.heading_up[idx] = not self.heading_up[idx]
                action = 3
            elif (not self.heading_up[idx] and y < len(self.free_map[0])-1 and
                obs[x][y+1] != self.free_map[x][y]):
                self.heading_up[idx] = not self.heading_up[idx]
                action = 1
            else:
                self.heading_up[idx] = not self.heading_up[idx]

        if (self.heading_right[idx] and x < len(self.free_map)-1 and
            obs[x+1][y] == self.free_map[x][y]):
            action = 2
        elif (not self.heading_right[idx] and x > 0 and
            obs[x-1][y] == self.free_map[x][y]):
            action = 4
        else:
            if (self.heading_right[idx] and x < len(self.free_map)-1 and
                obs[x+1][y] != self.free_map[x][y]):
                self.heading_right[idx] = not self.heading_right[idx]
                action = 4
            elif (not self.heading_right[idx] and x > 0 and
                obs[x-1][y] != self.free_map[x][y]):
                self.heading_right[idx] = not self.heading_right[idx]
                action = 2
            else:
                self.heading_right[idx] = not self.heading_right[idx]

        return action

        # in case it has reached the border
        # elif (y < 0 or y >= len(self.free_map[0])):
        #     self.heading_up[index] = not self.heading_up[index]
        #
        # else:
        #     if (self.heading_right[index] and
        #         x < len(self.free_map)-1 and
        #         obs[x+1][y] == self.free_map[x][y]):
        #         action = 2
        #     elif (not self.heading_right[index] and
        #         x > 0 and
        #         obs[x-1][y] == self.free_map[x][y]):
        #         action = 4




        # if (y <= 0 or y > len(self.free_map[0])):
        #     self.heading_up[index] = not self.heading_up[index]
        #
        # if (x <= 0 or x >= len(self.free_map)-1):
        #     self.heading_right[index] = not self.heading_right[index]
        #
        # if action == 1 and self.heading_up[index] == False:
        #     action = 3
        #
        # if action == 2 and self.heading_right[index] == False:
        #     action = 4

        # if action == 1:
        #     self.heading_up[index] = True
        #
        # if action == 2:
        #     self.heading_right[index] = True
        #     self.heading_up[index] = False
        #
        # # Now cases to set the direction of the player
        # if self.heading_right[index] == True:
        #     action = 2
        # else:
        #     action = 4
        #
        # if self.heading_up[index] == True:
        #     action = 1
        # else:
        #     action = 3

        # first make sure if there is an obstacle
        # if (x <=0 or x >= len(self.free_map)-1 or
        #     )
        # rand_action = random.choice(0, 5)
        # if obstacle at left then choose any direction except left

        # if (x>0 and obs[x-1][y] != self.free_map[x][y]):
        #     action = int(random.choice([0,1,2,3]))
        #
        # elif (x+1 < len(self.free_map) and obs[x+1][y] != self.free_map[x][y]):
        #     action = int(random.choice([0,1,4,3]))
        #
        # elif (y > len(self.free_map) and obs[x][y-1] != self.free_map[x][y]):
        #     action = int(random.choice([0,2,4,3]))
        #
        # elif (y < len(self.free_map) - 1 and obs[x][y+1] != self.free_map[x][y]):
        #     action = int(random.choice([0,1,4,2]))
