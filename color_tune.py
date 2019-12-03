import numpy as np
import gym
import ray
from ray import tune
from ray.tune import grid_search
from ray.tune.registry import register_env
from colorenv.colorenv import ColorEnv
import os

if __name__ == "__main__":
    path_to_config = os.getcwd() + "/colorenv/config.yml"

    register_env("coloring", lambda config: ColorEnv(path_to_config))
    ray.init()
    tune.run(
        "DQN",
        stop={"episode_reward_mean": 0.98},
        config={
            "env": "coloring",
            "schedule_max_timesteps": 1000000,
            # "exploration_fraction": tune.grid_search([.001, .01, .05, .1]),
            "exploration_fraction": .1,
            # "num_workers": tune.grid_search([0,1,2]),
            "num_workers": 0,
        },
    )
