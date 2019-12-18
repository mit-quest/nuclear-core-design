import gym
import yaml
import os
import random
import numpy as np
from gym import error, utils
from gym.spaces import Discrete, Box, Tuple
from gym.utils import seeding
from colorama import Fore

'''
calls _check_rep before and after the function to ensure it did not violate the invariants
'''
def check_rep_decorate(func):
    def func_wrapper(self,*args, **kwargs):
        # self._check_rep()
        out = func(self,*args, **kwargs)
        # self._check_rep()
        return out
    return func_wrapper

class FloatEnv(gym.Env):

    def __init__(self, path_to_config):
        # read in configuration file
        with open(path_to_config, "r") as yamlfile:
            config = yaml.safe_load(yamlfile)

            self.n = config['gym']['n'] # n is the sidelength of our square gameboard, must be greater than 1
            self.game_length = config['gym']['game_length'] # the number of increments to perform
            self.flatten = config['gym']['flatten'] # if true, flatttens the state to a 1d vector before returning
            self.cutoff = config['gym']['cutoff'] # the delta required between two pieces required for them to be "different colors"

            seed = config['gym']['seed']
            if (seed != None):
                random.seed(seed)

        # pick a location and a value to increment it by
        self.action_space = Tuple((Discrete(self.n ** 2), Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float16)))
        if self.flatten:
            self.observation_space = Box(low=-1.0, high=1.0, shape=(self.n * self.n,), dtype=np.float16)
        else:
            self.observation_space = Box(low=-1.0, high=1.0, shape=(self.n, self.n), dtype=np.float16)

        # and n x n array where each location is a piece value
        self.state = np.zeros((self.n, self.n), dtype=np.float16)

        self.counter = 0 # the number of actions the agent has taken
        self.done = False # true if environement has reached terminal state, false otherwise


    '''
    returns the view the agent gets of the state, which is either identical to the the internal
    state view or a flattened view depending on the self.flatten paramater set during config
    '''
    def _get_state_agent_view(self):
        if self.flatten:
            return self.state.flatten()
        else:
            return self.state

    '''
    validates that the internal representation is consistent with the design invariants
    '''
    def _check_rep(self):
        assert self.n > 0, "n must be positive and non-zero"
        assert self.game_length > 0, "game_length must be positive and non-zero"
        if self.done:
            assert self.counter == self.game_length, "the counter is not correct"
        else:
            assert self.counter < self.game_length, "the counter is not correct"

    '''
    return true if the two values differ by more than the cutoff and therefore represent different colors
    '''
    def _different_colors(self, value1, value2):
        return abs(value1 - value2) >= self.cutoff

    '''
    gets the current score of the board. Each piece is worth some fractional amount of reward based upon
    how many legal pieces (not within the cutoff) are next to it. This value is changed based upon self.n
    to ensure that the max reward is always 1
    '''
    @check_rep_decorate
    def _current_score(self):
        score = 0
        board = self.state

        # get the number of checks performed so the reward for each valid neighbor is 1/num_checks
        # which always makes the maximum reward 1
        num_checks = ((self.n - 1) ** 2) * 2 + 2
        increment = 1/num_checks

        # checks for all pieces (except the last column and row)
        # that if pieces below and to the right are not the same color
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                if self._different_colors(board[i, j], board[i+1, j]):
                    score += increment
                if self._different_colors(board[i, j], board[i, j+1]):
                    score += increment

        #check the bottom right corner against its two neighbors
        bot_right = board[self.n - 1, self.n - 1]
        if self._different_colors(bot_right, board[self.n - 2, self.n - 1]):
            score += increment
        if self._different_colors(bot_right, board[self.n - 1, self.n - 2]):
            score += increment

        return score

    '''
    takes in an agents intended action, update board state and increment coutner, returns state and score
    '''
    @check_rep_decorate
    def step(self, action):
        location, increment_val = action

        if self.done:
            print("Game is already over")
            return [self._get_state_agent_view(), 0, self.done, {}]

        self.counter += 1
        # check if game is over after this action
        if self.counter == self.game_length:
            self.done = True

        # since locations are in row major order
        row = location // self.n
        col = location % self.n

        # increment the location by the provided value and do bounds checking
        self.state[row, col] += increment_val
        if self.state[row, col] > 1:
            self.state[row, col] = 1
        if self.state[row, col] < -1:
            self.state[row, col] = -1

        return [self._get_state_agent_view(), self._current_score(), self.done, {}]

    '''
    resets the board
    '''
    @check_rep_decorate
    def reset(self):
        self.counter = 0
        self.done = 0
        self.state = np.zeros((self.n, self.n), dtype=np.float16)

        return self._get_state_agent_view()

    def render(self, mode='human', close=False, show_position_numbers=False):
        row_len = self.state.shape[0]

        print("Board state:")
        print(" " * 3, end="")

        for i in range(row_len):
            if i == row_len - 1:
                print("\033[4m"+ str(i) + "  \033[0m")
            else:
                print("\033[4m"+ str(i) + "   \033[0m", end="")

        for i,row in enumerate(self.state):
            print(i, end="| ")
            print(" ".join(map(lambda x: str(x), list(row))))
        print()

        if show_position_numbers:
            print("Position Numbers:")
            print(" " * 3, end="")

            for i in range(row_len):
                if i == row_len - 1:
                    print("\033[4m"+ str(i) + " \033[0m")
                else:
                    print("\033[4m"+ str(i) + "  \033[0m", end="")

            start = 0
            for i in range(row_len):
                print(i, end="| ")
                print(" ".join(map(lambda x: str(x) if x > 9 else str(x) + " ", range(start, start+row_len))))
                start += row_len
            print()
