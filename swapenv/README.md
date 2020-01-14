# Swap Environment
This environment simulates an N x N grid where each space is initialized to a random color. At every timestep the agent specifies two locations, which are swapped. At each timestep a reward between 0 and 1 is returned based upon how close the board is to a legal configuration.

### Running the random agent:
1. Run `source .venv/bin/activate` to enter the virtual environement
2. Run `python random_swap_agent.py`

### Running the examples:
1. Run `source .venv/bin/activate` to enter the virtual environement
2. Run `python swap_tune.py` to train a PPO agent on a 5x5 floating environment

### Visualization:
After running one of the tune scripts you can run `tensorboard --logdir=~/ray_results/` in another window to visualize training in your browser

### Playing the environment yourself:
You can run `python play.py` and interact with the environment yourself, the instructions are built in.
