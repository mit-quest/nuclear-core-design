This repository is under development. Expect anything in it to change rapidly.

# nuclear-core-design
### Install Procedure
1. Clone the repository and `cd` into it 
2. Run `make`

You have now successfully installed the repository!

### Running the random agents:
1. Run `source .venv/bin/activate` to enter the virtual environement
2. Navigate to the environment you want to test, either `swapenv`, `floatenv` or `colorenv`
3. Run the corresponding python script, for example: `python random_swap_agent.py`

### Running the examples:
1. Run `source .venv/bin/activate` to enter the virtual environement
2. Run `python test_tune.py` to see Rllib train a PPO agent on CartPole and perform a grid search for the best learning rate
3. Run `python color_tune.py` to train a DQN agent on a 3x3 coloring environment with 2 colors
4. Run `python swap_tune.py` to train a PPO agent on a 3x3 swap environment with 2 colors
4. Run `python float_tune.py` to train a PPO agent on a 5x5 float environment

### Visualization:
After running one of the tune scripts you can run `tensorboard --logdir=~/ray_results/` in another window to visualize training in your browser

### Playing the environment yourself:
Currently this is only supported by `swapenv` and `floatenv`. You can play by navigating to the `swapenv` or `floatenv` directory an running `python play.py`
