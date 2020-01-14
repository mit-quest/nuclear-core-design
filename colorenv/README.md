# Coloring Environment
This environment simulates an N x N grid that starts empty. At every timestep the environment randomly selects an empty position and the agent returns a color it wants to put in that position. The cycle repeats until there are no empty spaces at which point the board is scored. A reward of one is returned if no two of the same colors are adjacent and zero otherwise.

### Running the random agent:
1. Ensure you are in the `nuclear-core-design` directory
1. Run `source .venv/bin/activate` to enter the virtual environment
2. Run `python colorenv/random_coloring_agent.py`

### Running the examples:
1. Ensure you are in the `nuclear-core-design` directory
1. Run `source .venv/bin/activate` to enter the virtual environment
2. Run `python colorenv/color_tune.py` to train a DQN agent on a 3x3 coloring environment with 2 colors

### Visualization:
After running one of the tune scripts you can run `tensorboard --logdir=results` in another window to visualize training in your browser.
