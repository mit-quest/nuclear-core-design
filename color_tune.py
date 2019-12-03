import numpy as np
import gym
import ray
import os
import argparse
import pandas as pd
from ray import tune
from ray.tune import grid_search
from ray.tune.registry import register_env
from colorenv.colorenv import ColorEnv
import matplotlib.pyplot as plt

def plot_ave_reward(analysis):
    #TODO find a better way to take the average of arrays that may be of different lengths
    # maybe a running max_len that pads everything only as necessary?
    max_iters = 999999
    trials = analysis.trial_dataframes
    ave_reward = np.zeros((max_iters,))
    counts = np.zeros((max_iters,))
    all_rewards = dict()
    max_len = -1

    for key in trials:
        cur_reward = trials[key]["episode_reward_mean"].to_numpy()
        padded = np.pad(cur_reward, (0, max_iters-len(cur_reward)))
        increment = np.pad(np.ones(cur_reward.shape), (0, max_iters-len(cur_reward)))

        ave_reward += padded
        counts += increment
        max_len = max(max_len, len(cur_reward))

        last_part_path = key.split("/")[-1]
        all_rewards[last_part_path] = list(padded)

    all_rewards["average"] = list(ave_reward[:max_len]/counts[:max_len])
    x = [i for i in range(max_len)]

    plt.xlabel("Iteration Number")
    plt.ylabel("Averge Reward")
    plt.title("Average Reward Across All Trials per Iteration")
    plt.plot(x, all_rewards["average"][:max_len], label="average")
    #TODO add error bars here

    # for key in all_rewards:
    #     plt.plot(x, all_rewards[key][:max_len], label=key)
    # plt.legend()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train an RL agent on the coloring environment')
    parser.add_argument('-t', '--num_trials', metavar='N', type=int, default=1, help='The number of trials to run. If num_trials != 1 a plot \
            will be generated upon termination that shows the average reward graphed against all the trials.')
    args = parser.parse_args()

    path_to_config = os.getcwd() + "/colorenv/config.yml"

    register_env("coloring", lambda config: ColorEnv(path_to_config))
    ray.init()
    analysis = tune.run(
        "PPO",
        stop={"episode_reward_mean": 0.98},
        config={
            "env": "coloring",
            "num_workers": 0,
        },
        num_samples=args.num_trials,
    )

    if (args.num_trials != 1):
        plot_ave_reward(analysis)
