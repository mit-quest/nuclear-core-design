import numpy as np
import gym
import math
import ray
import pandas as pd
from ray import tune
from ray.tune import grid_search
from ray.tune.registry import register_env
from colorenv.colorenv import ColorEnv
import matplotlib.pyplot as plt

def plot_ave_reward(analysis):
    # hardcoded number of max iterations so that trials of different lengths can be padded to this length and stacked
    # eventually after the maximum trial length is found, all arrays are cut down to that length and extra zeros are discarded
    max_iters = 999999
    trials = analysis.trial_dataframes
    ave_reward = np.zeros((max_iters,))
    all_rewards = dict()
    max_len = -1

    for key in trials:
        cur_reward = trials[key]["episode_reward_mean"].to_numpy() # mean reward for this agent every iteration
        padded = np.pad(cur_reward, (0, max_iters-len(cur_reward)), mode='edge') # pad reward array so they can all be added together

        ave_reward += padded
        max_len = max(max_len, len(cur_reward))

        last_part_path = key.split("/")[-1]
        all_rewards[last_part_path] = padded

    ave_reward = list(ave_reward[:max_len]/len(all_rewards)) # get average reward for each iteration based upon how many agents reached that iteration
    x = [i for i in range(max_len)]
    rows = [arr[:max_len] for arr in all_rewards.values()]
    matrix = np.vstack(tuple(rows)) #stack all trials vertically so the sample standard deviation can be computed
    std = np.std(matrix,0)
    rootn = math.sqrt(matrix.shape[0])
    std_err = std/rootn # standard error of every iteration

    plt.xlabel("Iteration Number")
    plt.ylabel("Averge Reward")
    plt.title("Average Reward Across All Trials with Std Erorr Bars")
    plt.errorbar(x, ave_reward, yerr=std_err, ecolor='r', label="average")

    plt.show()


if __name__ == "__main__":
    import os
    import argparse

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
        config={
            "env": "coloring",
            "schedule_max_timesteps": 1000000,
            "exploration_fraction": .1,
            "num_workers": 0,
            "seed": args.seed,
        },
        num_samples=args.num_trials,
    )

    if (args.num_trials != 1):
        plot_ave_reward(analysis)
