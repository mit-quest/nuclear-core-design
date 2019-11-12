import gym
import colorenv
import statistics

rewards = []
num_iterations = 10000
env = gym.make("ColorEnv-v0")
observation = env.reset()

for _ in range(num_iterations):
  action = env.action_space.sample() # your agent here (this takes random actions)
  observation, reward, done, info = env.step(action)

  if done:
    rewards.append(reward)
    observation = env.reset()

env.close()
print("Average reward over {} iterations: {}".format(num_iterations, statistics.mean(rewards)))
