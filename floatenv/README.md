# Floating Environment
This environment simulates an N x N grid where each space is initialized to 0.0. At every timestep the agent selects a location and specifies an increment value (between -1 and 1), that location is then incremented by the specified value. At each timestep a reward between 0 and 1 is returned based upon how close the board is to a legal configuration.

### Running the random agent:
1. Ensure you are in the `nuclear-core-design` directory
2. Run `source .venv/bin/activate` to enter the virtual environement
3. Run `python floatenv/random_float_agent.py`

### Running the examples:
1. Ensure you are in the `nuclear-core-design` directory
2. Run `source .venv/bin/activate` to enter the virtual environement
3. Run `python any_tune.py -c /configs/float_default_config.yaml` to train a PPO agent on a 5x5 floating environment

### Playing the environment yourself:
You can run `python play.py` and interact with the environment yourself, the instructions are built in.

### Writing a config:
Below is a list of the paramaters that can be used to control the gym float environment.
* n: the length of the side of the square gameboard
* game_length: the number of actions the agent takes per episode
* seed: either null or an integer 
* flatten: true or false, if true, flattens the observation before passing it to the agent
* cutoff: the decimal (between 0 and 1) that two swquares must be different to be considered different colors
