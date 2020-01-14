# Floating Environment
This environment simulates an N x N grid where each space is initialized to 0.0. At every timestep the agent selects a location and specifies an increment value (between -1 and 1), that location is then incremented by the specified value. At each timestep a reward between 0 and 1 is returned based upon how close the board is to a legal configuration.

### Running the random agent:
1. Ensure you are in the `nuclear-core-design` directory
1. Run `source .venv/bin/activate` to enter the virtual environement
2. Run `python floatenv/random_float_agent.py`

### Running the examples:
1. Ensure you are in the `nuclear-core-design` directory
1. Run `source .venv/bin/activate` to enter the virtual environement
2. Run `python floatenv/float_tune.py` to train a PPO agent on a 5x5 floating environment

### Visualization:
After running one of the tune scripts you can run `tensorboard --logdir=~/ray_results/` in another window to visualize training in your browser

### Playing the environment yourself:
You can run `python play.py` and interact with the environment yourself, the instructions are built in.
