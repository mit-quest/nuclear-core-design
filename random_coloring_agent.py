import gym
import statistics
import os
from colorenv.colorenv import ColorEnv

rewards = []
num_iterations = 100000
path_to_config = os.getcwd() + "/colorenv/config.yaml"
env = ColorEnv(path_to_config)
observation = env.reset()

for _ in range(num_iterations):
  action = env.action_space.sample() # this takes random actions
  observation, reward, done, info = env.step(action)

  if done:
    rewards.append(reward)
    observation = env.reset()

env.close()
print("Average reward over {} iterations: {}".format(num_iterations, statistics.mean(rewards)))
