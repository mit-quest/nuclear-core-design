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

class SwapEnv(gym.Env):

    def __init__(self, path_to_config):
        # read in configuration file
        with open(path_to_config, "r") as yamlfile:
            config = yaml.safe_load(yamlfile)
            config = config['gym']

            continuous = config['continuous']
            if (continuous != None):
                self.shifting = True
                self.n = continuous['start']
                self.end = continuous['end']
                self.game_length = self.n ** 2
                self.logfile = continuous['logfile']
                self.shift_cutoff = continuous['cutoff']
                self.ema_n = continuous['ema_n']
                self.episode_reward = 0
                with open(self.logfile, "w") as f:
                    f.write("0.0") # initialize the EMA to 0

            else:
                self.shifting = False
                self.n = config['n'] # n is the sidelength of our square gameboard, must be greater than 1
                self.end = self.n
                self.game_length = config['game_length'] # the number of actions (swaps or null moves) to perform

            self.num_colors = config['num_colors'] # number of colors that the AI can choose from
            self.flatten = config['flatten'] # if true, flatttens the state to a 1d vector before returning

            seed = config['seed']
            if (seed != None):
                random.seed(seed)

        # whether to make the null move (no swap) as well as two locations (to swap if not null)
        self.action_space = Tuple((Discrete(1), Discrete(self.end ** 2), Discrete(self.end ** 2)))
        if self.flatten:
            self.observation_space = Box(low=0, high=self.num_colors+1, shape=(self.end * self.end,), dtype=np.int32)
        else:
            self.observation_space = Box(low=0, high=self.num_colors+1, shape=(self.end, self.end), dtype=np.int32)

        # and n x n array where the number represents a color, 1 is the first color, 2 is the second color, etc.
        self.state = np.zeros((self.end,self.end), dtype = int)
        self._generate_new_board()

        self.counter = 0 # the number of actions the agent has taken
        self.done = False # true if environement has reached terminal state, false otherwise


    def continuous_enabled(self):
        return self.shifting

    '''
    generates a fresh board position, attepts to place colors fairly. If the size of the board is divisible by
    the number of colors, an equal number of all colors will be placed, else, the first color will recieve the
    remainder. E.g. n=4 and 2 colors means 8 pieces of each color, while n=4 and 3 colors means 6,5, and 5 pieces respectively
    '''
    def _generate_new_board(self):
        board_size = self.n ** 2
        all_pieces = [1] * ((board_size // self.num_colors) + (board_size % self.num_colors))

        # start at 2 since colors are 1 indexed
        for color in range(2,self.num_colors + 1):
            addition = [color] * (board_size // self.num_colors)
            all_pieces.extend(addition)

        assert len(all_pieces) == board_size, "the all_pieces and board_size don't match in size"

        for i in range(self.n):
            for j in range(self.n):
                cur_piece = random.choice(all_pieces)
                all_pieces.remove(cur_piece)
                self.state[i,j] = cur_piece

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
        assert self.num_colors > 0, "num_colors must be positive and non-zero"
        assert self.game_length > 0, "game_length must be positive and non-zero"
        if self.done:
            assert self.counter == self.game_length, "the counter is not correct"
        else:
            assert self.counter < self.game_length, "the counter is not correct"

    '''
    gets the current score of the board. Each piece is worth some fractional amount of reward based upon
    how many legal pieces (not of the same color) are next to it. This value is changed based upon self.n
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
                if board[i, j] != board[i+1, j]:
                    score += increment
                if board[i, j] != board[i, j+1]:
                    score += increment

        #check the bottom right corner against its two neighbors
        bot_right = board[self.n - 1, self.n - 1]
        if bot_right != board[self.n - 2, self.n - 1]:
            score += increment
        if bot_right != board[self.n - 1, self.n - 2]:
            score += increment

        return score

    '''
    takes in an agents intended action, update board state and increment coutner, returns state and score
    '''
    @check_rep_decorate
    def step(self, action):
        null, loc1, loc2 = action
        if loc1 >= self.n ** 2 or loc2 >= self.n ** 2:
            return [self._get_state_agent_view(), 0, self.done, {}]

        if self.done:
            print("Game is already over")
            return [self._get_state_agent_view(), 0, self.done, {}]

        self.counter += 1
        # check if game is over after this action
        if self.counter == self.game_length:
            self.done = True

        if null != 1:
            # the agent has chosen not the make the null move and therefore to swap 2 pieces

            # since locations are in row major order
            row1 = loc1 // self.n
            col1 = loc1 % self.n
            row2 = loc2 // self.n
            col2 = loc2 % self.n

            # swap the pieces
            temp = self.state[row1, col1]
            self.state[row1, col1] = self.state[row2, col2]
            self.state[row2, col2] = temp

        cur_score = self._current_score()
        if self.shifting:
            self.episode_reward += cur_score

        return [self._get_state_agent_view(), cur_score, self.done, {}]

    '''
    resets the board
    '''
    @check_rep_decorate
    def reset(self):

        if self.shifting:
            # check the current value of the moving ave, if it meets the cutoff criterea then make the board larger and notify the user
            with open(self.logfile, "r+") as f:
                try:
                    text = f.read()
                    old_ema = float(text)
                except ValueError as e:
                    if text == "":
                        # someone else just tried to write 0
                        old_ema = 0.0
                    else:
                        print(e)
                        exit(0)

            k = 2 / (self.ema_n  + 1)
            new_ema = k * self.episode_reward + old_ema * (1 - k)

            if new_ema > (self.n ** 2) * self.shift_cutoff:
                with open(self.logfile, "w") as f:
                    f.write("0.0") #start ema fresh

                if self.n < self.end:
                    self.n += 1
                    self.game_length = self.n ** 2
                    print("New N:", self.n)
                    with open("current_n.txt", "a+") as f:
                        f.write(str(self.n))
            else:
                with open(self.logfile, "w") as f:
                    f.write(str(new_ema))

            self.episode_reward = 0

        self.counter = 0
        self.done = 0
        self._generate_new_board()

        return self._get_state_agent_view()

    def render(self, mode='human', close=False, show_position_numbers=False):
        row_len = self.state.shape[0]
        #warning, colors will begin to cycle if there are more than 6
        text_colors = [Fore.RED, Fore.BLUE, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]

        print("Board state:")
        print(" " * 3, end="")

        for i in range(row_len):
            if i == row_len - 1:
                print("\033[4m"+ str(i) + "\033[0m")
            else:
                print("\033[4m"+ str(i) + " \033[0m", end="")

        for i,row in enumerate(self.state):
            print(i, end="| ")
            print(" ".join(map(lambda x: text_colors[(x-1)%6] + str(x), list(row))))
            print(Fore.WHITE, end="")
        print()

        if show_position_numbers:
            if self.shifting:
                row_len = self.n
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
