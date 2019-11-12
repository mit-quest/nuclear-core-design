This repository is under development. Expect anything in it to change rapidly.

# nuclear-core-design
### Install Procedure
1. Clone the repository and `cd` into it 
2. Run `virtualenv venv` 
3. Run `source venv/bin/activate`
4. Run `pip install -r requirements.txt`

You have now successfully installed the repository!

### Running the examples:
1. Run `python random_agent.py` to get the average reward of a random agent in the coloring environment
2. Run `python test_tune.py` to see Rllib train a PPO agent on CartPole and perform a grid search for the best learning rate
