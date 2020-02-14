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
from swapenv.swapenv import SwapEnv
from floatenv.floatenv import FloatEnv
from colorenv.colorenv import ColorEnv
from bwr6x6env.bwr6x6env import BWR6x6Env
from util import plot_ave_reward, eval_unpack, debug_config_print

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train an RL agent on the specified environment')
    parser.add_argument(
        '-c', '--config',
        metavar='PATH',
        type=str,
        default="configs/swap_default_config.yaml",
        help="read in tune arguments from specified config file, e.g. '/configs/swap_default_config.yaml'")
    parser.add_argument(
        '-d', '--debug-config',
        action='store_true',
        help='turns on the debug print')
    args = parser.parse_args()

    path_to_config = str(pathlib.Path(__file__).parent.parent.absolute()) + '/' + args.config
    print(path_to_config)

    register_env("swap", lambda config: SwapEnv(path_to_config))
    register_env("float", lambda config: FloatEnv(path_to_config))
    register_env("color", lambda config: ColorEnv(path_to_config))
    register_env("bwr6x6", lambda config: BWR6x6Env(path_to_config))
    ray.init(webui_host="0.0.0.0")

    with open(path_to_config, "r") as yamlfile:
        config = yaml.safe_load(yamlfile)
        if args.debug_config:
            debug_config_print(config)

    if config['to_eval'] != None:
        eval_unpack(config['tune'], config['to_eval'])

    analysis = tune.run(config['algorithm'], **config['tune'])

    if (config['tune']['num_samples'] != 1):
        plot_ave_reward(analysis)
