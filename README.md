This repository is under development. Expect anything in it to change rapidly.

# nuclear-core-design
## Install Procedure
1. Clone the repository and `cd` into it 
2. Run `make`

You have now successfully installed the repository!

## Running the test example:
1. Run `source .venv/bin/activate` to enter the virtual environment
2. Run `python test_tune.py` to see Rllib train a PPO agent on CartPole and perform a grid search for the best learning rate

## Environments

### Coloring Environment

The purpose of the Coloring Environment is to serve as an optimization test over a parameterized number of discrete variables. See a detailed description of the environment and how to run agents in it [here](colorenv/README.md).

### Float Environment

The purpose of the Float Environment is to serve as an optimization test over a parameterized number of continuous variables. See a detailed description of the environment and how to run agents in it [here](floatenv/README.md).

## Visualization:
After running one of the tune scripts you can run `tensorboard --logdir=results` in another window to visualize training in your browser.

