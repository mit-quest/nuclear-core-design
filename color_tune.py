import os
import argparse
import gym
import math
import ray
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ray import tune
from ray.tune import grid_search
from ray.tune.registry import register_env
from colorenv.colorenv import ColorEnv
from util import plot_ave_reward

count = 0
search_values = [.01, .1, .2]
param_name = "exploration_fraction"

def get_trial_name(trial):
    if param_name is not None:
        global count
        trial_name = "{}={}_".format(param_name, search_values[count % len(search_values)]) + str(trial)
        count += 1
        return trial_name

    return trial

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train an RL agent on the coloring environment')
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
    args = parser.parse_args()

    path_to_config = os.getcwd() + "/colorenv/config.yaml"

    register_env("coloring", lambda config: ColorEnv(path_to_config))
    ray.init()
    analysis = tune.run(
        "DQN",
        stop={"episode_reward_mean": 0.98},
        trial_name_creator=get_trial_name,
        config={
            "env": "coloring",
            "schedule_max_timesteps": 1000000,
            param_name: tune.grid_search(search_values),
            "num_workers": 0,
            "seed": args.seed,
        },
        num_samples=args.num_trials,
        checkpoint_freq = 10,
        checkpoint_at_end=True,
        max_failures = 5,
    )

    if (args.num_trials != 1):
        plot_ave_reward(analysis)
