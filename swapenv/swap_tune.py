import os
import pathlib
os.environ["TUNE_RESULT_DIR"] = pathlib.Path("./results").absolute().as_posix()  # tells tune to log in nuclear-core-design/results
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
from util import plot_ave_reward, eval_unpack

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train an RL agent on the swap environment')
    parser.add_argument(
        '-c', '--config',
        metavar='PATH',
        type=str,
        default="/configs/swap_default_config.yaml",
        help="read in tune arguments from specified config file")
    args = parser.parse_args()

    path_to_config = str(pathlib.Path(__file__).parent.parent.absolute()) + args.config

    register_env("swap", lambda config: SwapEnv(path_to_config))
    ray.init(webui_host="0.0.0.0")

    with open(path_to_config, "r") as yamlfile:
        config = yaml.safe_load(yamlfile)

    if config['to_eval'] != None:
        eval_unpack(config['tune'], config['to_eval'])

    analysis = tune.run(config['algorithm'], **config['tune'])

    if (config['tune']['num_samples'] != 1):
        plot_ave_reward(analysis)
