from gym.envs.registration import register

register(
    id='ColorEnv-v0',
    entry_point='colorenv.colorenv:ColorEnv',
)

