from gym.envs.registration import register

register(
    id='SwapEnv-v0',
    entry_point='swapenv.swapenv:SwapEnv',
)

