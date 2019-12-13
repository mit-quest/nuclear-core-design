import os
import math
import json
import datetime
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

def create_dict(filename):
    loaded = json.load(open(filename))
    result = dict()
    for key in loaded:
        result[key] = pd.read_json(loaded[key])
    return result

def get_params(trial_path):
    return json.load(open(trial_path + "/params.json"))

def get_varied_param(trial_dict):
    '''
    Returns the name of the paramater which was varied using tune.grid_search
    If no such paramater or multiple such paramaters exist, return None
    Also return the set of values that varied param takes if it exists, None if not
    '''
    #gather each paramater into its own set, if all sets are length one, proceed as normal,
    #otherwise if only one is length > 1, return name and values, if more than one are len > 1
    #treat the data as if no params have been varied and return two None
    param_sets = defaultdict(set) # maps param names to sets of values
    for trial_path in trial_dict.keys():
        params = get_params(trial_path)
        for param in params:
            param_sets[param].add(params[param])

    params_varied = False
    varied_param_name = None
    for param in param_sets:
        if not params_varied and len(param_sets[param]) != 1:
            params_varied = True
            varied_param_name = param
        elif len(param_sets[param]) != 1:
            print("More than one param has been varied. Plotting all trials as one line.")
            params_varied = False
            break

    return varied_param_name, param_sets[varied_param_name] if params_varied else None, None

def get_reward_matrix_and_dict(trial_dict):
    '''
    Given a dicionary mapping trial paths to dataframes, return a 2 dimensionaly numpy array where:
        each row is a trial's full history of mean reward acquired
        each column is one full training iteration
    Also return a dictionary mapping trial_paths to the array of their mean reward recieved

    Note that if all the trials are not of the same length, they will all be padded by exending the last value
    to the maximum length among all trials so they can be vertically stacked. This is equivalent to letting the
    converged models continue to run (assuming they would continue to output the same converged reward)
    '''
    # hardcoded number of max iterations so that trials of different lengths can be padded to this length and stacked
    # eventually after the maximum trial length is found, all arrays are cut down to that length and extra zeros are discarded
    max_iters = 999999
    ave_reward = np.zeros((max_iters,))
    all_rewards = dict()
    max_len = -1

    for trial_path in trial_dict:
        cur_reward = trial_dict[trial_path]["episode_reward_mean"].to_numpy() # mean reward for this agent every iteration
        assert len(cur_reward) <= max_iters, "number of iterations in trial exceeds max_iters"
        padded = np.pad(cur_reward, (0, max_iters-len(cur_reward)), mode='edge') # pad reward array so they can all be added together

        max_len = max(max_len, len(cur_reward))

        all_rewards[trial_path] = padded

    for trial_path in all_rewards:
        #cut all the padded rows down to size now that we know the max_len
        all_rewards[trial_path] = all_rewards[trial_path][:max_len]

    reward_matrix = np.vstack(tuple(all_rewards.values()))

    return reward_matrix, all_rewards

def get_ave_reward(reward_matrix):
    return np.mean(reward_matrix, axis=0)

def get_x_array(reward_matrix):
    max_len = reward_matrix.shape[1]
    return [i for i in range(max_len)]

def get_std_error(reward_matrix):
    std = np.std(reward_matrix, 0)
    rootn = math.sqrt(reward_matrix.shape[0])
    return std/rootn # standard error of every iteration

def get_reward_matrix_given_param(all_rewards, param_name, param_value):
    all_rows = []
    for trial_path in all_rewards:
        if get_params(trial_path)[param_name] == param_value:
            all_rows.append(all_rewards[trial_path])

    return np.vstack(tuple(all_rows))

def plot_ave_reward(analysis):
    '''
    Takes in a tune analysis object (https://ray.readthedocs.io/en/latest/tune-package-ref.html#ray.tune.Analysis)
    and plots the average reward over all iterations as well as the standard error. If a tune.grid_search
    was performed over exactly one paramater, one line (as its corresponding error bars) is plotted for each
    value of that paramater.
    '''
    all_trials = analysis.trial_dataframes

    reward_matrix, all_rewards = get_reward_matrix_and_dict(all_trials)
    temp = get_varied_param(all_trials)
    varied_param, param_values = temp[0], temp[1]

    plt.xlabel("Iteration Number")
    plt.ylabel("Averge Reward")
    plt.title("Average Reward Across All Trials with Std Error Bars")

    if varied_param is not None:
        #plot multiple lines, one for each value of varied_param
        x = get_x_array(reward_matrix)

        colors = iter(cm.rainbow(np.linspace(0,1,len(param_values))))

        for value in param_values:
            cur_reward_matrix = get_reward_matrix_given_param(all_rewards, varied_param, value)
            ave_reward = get_ave_reward(cur_reward_matrix)
            std_err = get_std_error(cur_reward_matrix)

            c=next(colors)
            plt.errorbar(x, ave_reward, color=c, yerr=std_err, ecolor='r', label=varied_param + ": {}".format(value))

        plt.legend()

    else:
        #plot one line
        x = get_x_array(reward_matrix)
        ave_reward = get_ave_reward(reward_matrix)
        std_err = get_std_error(reward_matrix)

        plt.errorbar(x, ave_reward, yerr=std_err, ecolor='r', label="average")

    if "plots" not in os.listdir():
        os.mkdir("plots")

    timestamp = datetime.datetime.now().strftime("%H-%M-%S-%m-%d-%Y")
    filename = "plots/ave_reward_{}.png".format(timestamp)
    plt.grid()
    plt.savefig(filename, dpi=600)
    print("\nPlot saved to: " + filename + "\n")
    plt.plot()
