import gym
import os
from bwr6x6env import BWR6x6Env

def get_user_action(env):
    env.render()
    print("What enrichment would you like this rod to have? 1 for high, 0 for low")
    str_action = input()
    if str_action != "0" and str_action != "1":
        return None

    return int(str_action)


if __name__ == '__main__':
    path_to_config = os.getcwd() + "/../configs/bwr6x6_default_config.yaml"
    env = BWR6x6Env(path_to_config)
    observation = env.reset()
    total_reward = 0
    actions_taken = 0
    print("Current board score: ", env._current_score())
    print("Next location: ", observation)

    while True:
        action = get_user_action(env)
        if action == None:
            print("That is not a valid action. Please retry:")
            continue

        print("Action taken: ", action)
        state, reward, done, other = env.step(action)
        total_reward += reward
        actions_taken += 1

        print("Reward recieved: ", reward)
        print("Average reward: ", total_reward/actions_taken)
        print("Total Reward: ", total_reward)
        print("Number of actions: ", actions_taken)
        print("\nNext location: ", state)

        if done:
            print("You reached the maximum number of actions, the game has ended.\n")
            # print final board state
            print("Final ", end="")
            env.render()

            break
