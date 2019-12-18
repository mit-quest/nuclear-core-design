from gym.envs.registration import register

register(
    id='FloatEnv-v0',
    entry_point='floatenv.floatenv:FloatEnv',
)

