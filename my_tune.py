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
        "PPO",
        stop={"episode_reward_mean": .9},
        config={
            "env": "coloring",
            "lr": 1e-2,
            "num_workers": 7,  # parallelism
        },
    )
