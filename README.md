This repository is under development. Expect anything in it to change rapidly.

# nuclear-core-design
### Install Procedure
1. Clone the repository and `cd` into it 
2. Run `make`

You have now successfully installed the repository!

### Running the examples:
1. Run `source venv/bin/activate` to enter the virtual environement
2. Run `python random_agent.py` to get the average reward of a random agent in the coloring environment
3. Run `python test_tune.py` to see Rllib train a PPO agent on CartPole and perform a grid search for the best learning rate
4. Run `python color_tune.py` to train a DQN agent on a 3x3 coloring environment with 2 colors

### Visualization:
After running `python test_tune.py` or `python color_tune.py` you can run `tensorboard --logdir=~/ray_results/` in another window to visualize training in your browser
