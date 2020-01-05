This repository is under development. Expect anything in it to change rapidly.

# nuclear-core-design
### Install Procedure
1. Clone the repository and `cd` into it 
2. Run `make`

You have now successfully installed the repository!

### Running the test example:
1. Run `source .venv/bin/activate` to enter the virtual environement
2. Run `python test_tune.py` to see Rllib train a PPO agent on CartPole and perform a grid search for the best learning rate

### Visualization:
After running one of the tune scripts you can run `tensorboard --logdir=~/ray_results/` in another window to visualize training in your browser
