import os
import pathlib
os.environ["TUNE_RESULT_DIR"] = str(pathlib.Path().absolute()) + "/results" # tells tune to log in nuclear-core-design/results
import sys
import argparse
import gym
import math
import ray
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ray import tune
from ray.tune import grid_search
from ray.tune.registry import register_env
from swapenv import SwapEnv
sys.path.append(".")
from util import plot_ave_reward

count = 0
# search_values = [1, 2, 3, 4]
# param_name = "num_workers"
param_name = None

def get_trial_name(trial):
    if param_name is not None:
        global count
        trial_name = "{}={}_".format(param_name, search_values[count % len(search_values)]) + str(trial)
        count += 1
        return trial_name

    return str(trial)

def eval_unpack(config, to_eval):
    '''
    takes all key/values pairs in to_eval and stores the eval'd values and corresponding keys
    in config while taking into account the nesting of to_eval

    config: the dictionary to add the eval'd key/value pairs to
    to_eval: the dictionary to iterate though to get key/value pairs (can be nested)
    '''
    for key, value in to_eval.items():
        if isinstance(value, dict):
            eval_unpack(config[key], value)
        else:
            config[key] = eval(value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train an RL agent on the swap environment')
    parser.add_argument(
        '-t',
        '--num_trials',
        metavar='N',
        type=int,
        default=1,
        help=('The number of trials to run. If num_trials != 1 a plot will be generated upon termination that shows '
              'the average reward graphed against all the trials.'))
    parser.add_argument(
        '-s', '--seed',
        metavar='N',
        type=int,
        default=None,
        help="specify a seed to Rllib to make training reproducible")
    parser.add_argument(
        '-c', '--config',
        action='store_true',
        help="read in tune arguments from config file instead of defaults in .py file")
    args = parser.parse_args()

    path_to_config = str(pathlib.Path(__file__).parent.absolute()) + "/config.yaml"

    register_env("swap", lambda config: SwapEnv(path_to_config))
    ray.init(webui_host="0.0.0.0")
    analysis = None

    if args.config:
        #run tune with the values from the config file
        with open(path_to_config, "r") as yamlfile:
            config = yaml.safe_load(yamlfile)

        if config['to_eval'] != None:
            eval_unpack(config['tune'], config['to_eval'])

        analysis = tune.run(config['algorithm'],
                # trial_name_creator=get_trial_name,
                # trial_name_creator=eval(config['trial_name_creator']),
                **config['tune'])

        if (config['tune']['num_samples'] != 1):
            plot_ave_reward(analysis)

    else:
        # run tune with the values provided here
        analysis = tune.run(
            "PPO",
            stop={"episode_reward_mean": 8},
            trial_name_creator=get_trial_name,
            config={
                "env": "swap",
                # "model": {"dim": 5, "conv_filters": [[16, [3, 3], 1]]},
                # "schedule_max_timesteps": 1000000,
                # param_name: tune.grid_search(search_values),
                "num_workers": 7,
                "seed": args.seed,
            },
            num_samples=args.num_trials,
            checkpoint_freq = 10,
            checkpoint_at_end=True,
            max_failures = 5,
        )

        if (args.num_trials != 1):
            plot_ave_reward(analysis)
