import gym
import yaml
import os
import random
import pickle
import numpy as np
from gym import error, utils
from gym.spaces import Discrete, Box, Tuple
from gym.utils import seeding
from colorama import Fore

class BWR6x6Env(gym.Env):

    def __init__(self, path_to_config):
        with open(path_to_config, "r") as yamlfile:
            config = yaml.safe_load(yamlfile)

            self.game_length = config['gym']['game_length'] # the number of actions to perform per episode
            pickle_file = config['gym']['pickle_file'] # the name of the pickled file that stores the objective function

            # a dictionary from state to reward value
            pickled_objective_func_path = "/".join(__file__.split("/")[:-1]) + "/" + pickle_file
            self.objective_func = pickle.load(open(pickled_objective_func_path, "rb"))


            seed = config['gym']['seed']
            if (seed != None):
                random.seed(seed)

        # one increase enrichment and one decrease enrichment action for each of the 21 positions
        self.action_space = Discrete(21 * 2)
        # either high or low enrichment at each of the 21 positions
        self.observation_space = Box(low=0, high=1, shape=(21,), dtype=np.int32)

        self.state = np.zeros((21,)) # start all positions at low enrichment

        self.counter = 0 # the number of actions the agent has taken
        self.done = False # true if environement has reached terminal state, false otherwise

    '''
    return the current reward based upon the objective function described in the readme
    note that the function has been changed so it should be maximized instead of minimized
    and the possible rewards have been scaled between 0 and 1 (also note that a layout that violates
    the constraints will get a reward of 0)
    '''
    def _current_score(self):
        key = tuple(self.state)
        return self.objective_func[key]

    '''
    takes in an agents intended action, update board state and increment coutner, returns state and score
    '''
    def step(self, action):
        if self.done:
            print("Game is already over")
            return [self.state, 0, self.done, {}]

        self.counter += 1
        # check if game is over after this action
        if self.counter == self.game_length:
            self.done = True

        location = action % 21 # get the location, space 0 through 20
        up_enrichment = action >= 21 # increment enrichment if aciton is 21-41, decrement if 0-20
        self.state[location] = 1 if up_enrichment else 0

        return [self.state, self._current_score(), self.done, {}]

    '''
    resets the board
    '''
    def reset(self):
        self.counter = 0
        self.done = 0
        self.state = np.zeros((21,))

        return self.state

    def render(self, mode='human', close=False):
        print(self.state)
