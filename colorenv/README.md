# Coloring Environment
This environment simulates an N x N grid that starts empty. At every timestep the environment randomly selects an empty position and the agent returns a color it wants to put in that position. The cycle repeats until there are no empty spaces at which point the board is scored. A reward of one is returned if no two of the same colors are adjacent and zero otherwise.

### Running the random agent:
1. Ensure you are in the `nuclear-core-design` directory
2. Run `source .venv/bin/activate` to enter the virtual environment
3. Run `python colorenv/random_coloring_agent.py`

### Running the examples:
1. Ensure you are in the `nuclear-core-design` directory
2. Run `source .venv/bin/activate` to enter the virtual environment
3. Run `python colorenv/color_tune.py` to train a DQN agent on a 3x3 coloring environment with 2 colors
3. Run `python any_tune.py -c /configs/color_default_config.yaml` to train a PPO agent on a 3x3 coloring environment

### Writing a config:
Below is a list of the paramaters that can be used to control the gym coloring environment.
* n: the length of the side of the square gameboard
* num_colors: the number of colors to populate the board with
* game_length: the number of actions the agent takes per episode
* seed: either null or an integer 
* flatten: true or false, if true, flattens the observation before passing it to the agent
* maximize_red: true or false, earn reward for ever color 1 piece placed in addition to a large negative reward if board is not legal
* disable_checking: true or false, turns off legality checking, often used with maximize_red when debugging
