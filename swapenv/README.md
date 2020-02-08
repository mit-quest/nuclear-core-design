# Swap Environment
This environment simulates an N x N grid where each space is initialized to a random color. At every timestep the agent specifies two locations, which are swapped. At each timestep a reward between 0 and 1 is returned based upon how close the board is to a legal configuration.

### Running the random agent:
1. Ensure you are in the `nuclear-core-design` directory
2. Run `source .venv/bin/activate` to enter the virtual environement
3. Run `python swapenv/random_swap_agent.py`

### Running the examples:
1. Ensure you are in the `nuclear-core-design` directory
2. Run `source .venv/bin/activate` to enter the virtual environement
3. Run `python any_tune.py -c configs/swap_default_config.yaml` to train a PPO agent on a 3x3 swap environment

### Playing the environment yourself:
You can run `python play.py` and interact with the environment yourself, the instructions are built in.

### Writing a config:
Below is a list of the paramaters that can be used to control the gym swap environment.
* n: the length of the side of the square gameboard
* num_colors: the number of colors to populate the board with
* game_length: the number of actions the agent takes per episode
* seed: either null or an integer 
* flatten: true or false, if true, flattens the observation before passing it to the agent
* continuous: null or a dict of more params, if non null this param overrides n and game_length
  * start: the starting value of n
  * end: the ending value of n
  * cutoff: the percentage (between 0 and 1) of max reward required to increment the current board size by 1
  * ema_n: the number of episodes to consdier in the exponential moving average that is compared to the cutoff
