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

            self.amplify_score = config['gym']['amplify_score'] # whether or not to amplify the score of optimal configurations
            pickle_file = config['gym']['pickle_file'] # the name of the pickled file that stores the objective function

            # a dictionary from state to reward value
            pickled_objective_func_path = "/".join(__file__.split("/")[:-1]) + "/" + pickle_file
            self.objective_func = pickle.load(open(pickled_objective_func_path, "rb"))


            seed = config['gym']['seed']
            if (seed != None):
                random.seed(seed)

        # one increase enrichment and one decrease enrichment action
        self.action_space = Discrete(2)
        # the location of the next rod to choose enrichment for
        self.observation_space = Discrete(21)

        self.state = np.zeros((21,)) # start all positions at low enrichment

        self.counter = 0 # the number of actions the agent has taken
        self.done = False # true if environement has reached terminal state, false otherwise

        self._new_free_coords()
        self._first_location()
        self.total_reward = 0

    def _new_free_coords(self):
        self.free_coords = set() # a set of all the remaining coordinates to put pieces in
        for i in range(21):
            self.free_coords.add(i)

    '''
    gets the first location to choose enrichment of
    '''
    def _first_location(self):
        # set the first location in the placement array
        self.current_loc = random.choice(tuple(self.free_coords)) # the next location to place a piece at
        self.free_coords.remove(self.current_loc)

    '''
    gets a new location from the free_coords set
    '''
    def _get_next_location(self):
        assert len(self.free_coords), "free_coords is empty, there are no more positions availble"

        # get new location and remove it from future options
        self.current_loc = random.choice(tuple(self.free_coords))
        self.free_coords.remove(self.current_loc)

    '''
    return the current reward based upon the objective function described in the readme
    note that the function has been changed so it should be maximized instead of minimized
    and the possible rewards have been scaled between 0 and 1 (also note that a layout that violates
    the constraints will get a reward of 0)
    '''
    def _current_score(self):
        key = tuple(self.state)
        score = self.objective_func[key]
        if score == 62.5 and self.counter == 21:
            print("Optimal Found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # return 500
        return score

    '''
    takes in an agents intended action, update board state and increment coutner, returns state and score
    '''
    def step(self, action):
        if self.done:
            print("Game is already over")
            return [self.current_loc, 0, self.done, {}]

        self.state[self.current_loc] = action

        self.counter += 1
        score = self._current_score()
        self.total_reward += score

        # check if game is over after this action
        if self.counter == 21:
            self.done = True
            if self.amplify_score:
                score *= score * score
                score /= 10000
        else:
            score = 0
            self._get_next_location()


        return [self.current_loc, score, self.done, {}]

    '''
    resets the board
    '''
    def reset(self):
        self.counter = 0
        self.done = 0
        self.state = np.zeros((21,))

        self._new_free_coords()
        self._first_location()
        self.total_reward = 0

        return self.current_loc

    def render(self, mode='human', close=False):
        print(self.state)
