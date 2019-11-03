import gym
import yaml
import numpy as np
import random
from gym import error, spaces, utils
from gym.utils import seeding
import os

'''
calls _check_rep before and after the function to ensure it did not violate the invariants
'''
def check_rep_decorate(func):
    def func_wrapper(self,*args, **kwargs):
        self._check_rep()
        out = func(self,*args, **kwargs)
        self._check_rep()
        return out
    return func_wrapper

class ColorEnv(gym.Env):

    def __init__(self):
        # read in configuration file
        with open("colorenv/config.yml", "r") as ymlfile:
            config = yaml.safe_load(ymlfile)

            self.n = config['gym']['n'] # n is the sidelength of our square gameboard, must be greater than 1
            self.num_colors = config['gym']['num_colors'] # number of colors that the AI can choose from
            self.maximize_red = config['gym']['maximize_red'] # enables different reward scheme, 1 for every red placement, -100 for invalid layout at the end

            seed = config['gym']['seed']
            if (seed != None):
                random.seed(seed)

        self.free_coords = set() # a set of all the remaining coordinates to put pieces in
        for i in range(self.n):
            for j in range(self.n):
                self.free_coords.add((i,j))

        # two n x n arrays stacked on top of each other, the first is the gameboard where 0 = no piece
        # and any other number represents the color at that location
        # the second array is the placement array, which is all zero except one 1 in the next location to put a piece in
        self.state = np.zeros((self.n,self.n,2), dtype = int)

        self.counter = 0 # the number of pieces that have been placed
        self.done = False # true if environement has reached terminal state, false otherwise
        self.current_loc = random.choice(tuple(self.free_coords)) # the next location to place a piece at

        # set the first location in the placement array
        self.free_coords.remove(self.current_loc)
        self.state[self.current_loc[0],self.current_loc[1],1] = 1


    '''
    gets the number of non-zero elements in the provided array
    '''
    def _num_nonzero(self,arr):
        return len(np.transpose(np.nonzero(arr)))

    '''
    validates that the internal representation is consistent with the design invariants
    '''
    def _check_rep(self):
        assert self.n > 0, "n must be positive and non-zero"
        if self.done:
            assert len(self.free_coords) == 0, "there are still coords remaining"
            assert self._num_nonzero(self.state[:,:,0]) == self.n ** 2, "there are empty spaces"
            assert self.counter == self.n ** 2, "the counter is not correct"
        else:
            num_pieces = self._num_nonzero(self.state[:,:,0])
            assert num_pieces != self.n ** 2, "the board is filled but not marked as done"
            assert num_pieces == self.counter, "the count is off"
            assert self._num_nonzero(self.state[:,:,1]) == 1, "there none or too many current placement locations specified"


    '''
    gets a new location from the free_coords set and sets the old location to
    zero while setting the new location to one in the placement array
    '''
    @check_rep_decorate
    def _get_next_location(self):
        assert len(self.free_coords), "free_coords is empty, there are no more positions availble"

        # get new location and remove it from future options
        new_loc = random.choice(tuple(self.free_coords))
        self.free_coords.remove(new_loc)

        # set old location in placement array to 0, set new location to 1
        self.state[self.current_loc[0],self.current_loc[1],1] = 0
        self.current_loc = new_loc
        self.state[self.current_loc[0],self.current_loc[1],1] = 1

    '''
    checks if the given location tuple (x,y) is inside of the n x n board and returns boolean accordingly
    '''
    @check_rep_decorate
    def _is_valid_location(location):
        return location[0] >= 0 and location[0] < self.n and location[1] >= 0 and location[1] < self.n

    '''
    assumes that the board is full of pieces, i.e. that self.counter == self.n * self.n
    checks if the board is in a legal configuration according to the self.num_colors coloring rule
    returns false if illegal board configuration, true if legal board configuration
    '''
    @check_rep_decorate
    def _check_legal_board(self):
        board = self.state[:,:,0]

        # checks for all pieces (except the last column and row)
        # that the pieces below and to the right are not the same color
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                if board[i, j] == board[i+1, j] or board[i, j] == board[i, j+1]:
                    return False

        #check the bottom right corner against its two neighbors
        bot_right = board[self.n - 1, self.n - 1]
        if bot_right == board[self.n - 2, self.n - 1] or bot_right == board[self.n - 1, self.n - 2]:
            return False

        return True

    '''
    takes in an agents intended action, update board state and increment coutner
    if board is full, i.e. self.counter == self.n * self.n then check if
    the board is in a legal configuration, returning a reward of 1 or 0 if not valid
    '''
    @check_rep_decorate
    def step(self, action):
        assert action <= self.num_colors, "this color is not legal"

        if self.done:
            print("Game is already over")
            return [self.state, 0, self.done, None]

        self.counter += 1
        self.state[self.current_loc[0],self.current_loc[1],0] = action
        reward = 1 if self.maximize_red and action == 1 else 0

        # check if game is over
        if self.counter == self.n ** 2:
            self.done = True
            self.state[self.current_loc[0], self.current_loc[1], 1] = 0
            if self._check_legal_board():
                reward = 1
            else:
                reward = -100 if self.maximize_red else 0

        else:
            self._get_next_location()

        return [self.state, reward, self.done, None]

    '''
    resets the board to be entirely empty with a random next placement location
    '''
    @check_rep_decorate
    def reset(self):
        for i in range(self.n):
            for j in range(self.n):
                self.free_coords.add((i,j))

        self.state = np.zeros((self.n, self.n, 2), dtype = int)
        self.counter = 0
        self.done = 0
        self.current_loc = random.choice(tuple(self.free_coords)) # the next location to place a piece at

        # set the first location in the placement array
        self.free_coords.remove(self.current_loc)
        self.state[self.current_loc[0],self.current_loc[1],1] = 1

        return self.state

    @check_rep_decorate
    def render(self, mode='human', close=False):
        print("Board state:")
        print(self.state[:,:,0])
        print("Placement array:")
        print(self.state[:,:,1])
        print()
