import numpy as np
import gym
import ray
from ray import tune
from ray.tune import grid_search
from ray.tune.registry import register_env
from colorenv.colorenv import ColorEnv

if __name__ == "__main__":
    register_env("coloring", lambda config: ColorEnv())
    ray.init()
    tune.run(
        "DQN",
        stop={"episode_reward_mean": .95},
        config={
            "env": "coloring",
            # "model": {"dim":2, "conv_filters": [[4, [2,2], 1], [4, [2,2], 1]]},
            # "entropy_coeff": tune.grid_search([.001, .01, .05, .1, .2]),
            # "entropy_coeff": tune.grid_search([.2, .3, .4, .5, .6]),
            # "exploration_fraction": 0.3,
            "schedule_max_timesteps": 1000000,
            "exploration_fraction": tune.grid_search([.001, .01, .05, .1, .2]),
            # "lr": tune.grid_search([0.05, 0.005]),
            # "lr": 1e-2,
            # "num_workers": 15,
            # "log_level": "DEBUG",
        },
    )
