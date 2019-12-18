import gym
import os
from floatenv import FloatEnv

def get_user_action(env):
    env.render(show_position_numbers=True)
    print("What action would you like to take? Enter a location and an increment value:")
    str_action = input().strip(" ")

    locations = str_action.split(" ")
    if len(locations) != 2:
        return None

    return (int(locations[0]), float(locations[1]))

if __name__ == '__main__':
    path_to_config = os.getcwd() + "/config.yaml"
    env = FloatEnv(path_to_config)
    observation = env.reset()
    total_reward = 0
    actions_taken = 0
    print("Current board score: ", env._current_score())

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

        if done:
            break

    print("You reached the maximum number of actions, the game has ended.\n")

    # print final board state
    print("Final ", end="")
    env.render()
