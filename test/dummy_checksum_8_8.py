import gym
import gym_fuzz1ng  # noqa F401
import numpy as np


def main():
    env = gym.make('FuzzChecksum_8_8-v0')
    print("dict_size={} eof={}".format(env.dict_size(), env.eof()))

    env.reset()

    inputs = [
        [
            42, 0, 0, 0, 0, 0, 0, 0, 0,
            43, 0, 0, 0, 0, 0, 0, 0, 0,
            44, 0, 0, 0, 0, 0, 0, 0, 0,
            45, 0, 0, 0, 0, 0, 0, 0, 0,
            46, 0, 0, 0, 0, 0, 0, 0, 0,
            47, 0, 0, 0, 0, 0, 0, 0, 0,
            48, 0, 0, 0, 0, 0, 0, 0, 0,
            49, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
    ]

    for i in inputs:
        obs, reward, done, info = env.step(np.array(i))

        print(("STEP:" +
               "step={}/{}/{} " +
               "action={} transitions={}").format(
                   info['step_coverage'].skip_path_count(),
                   info['step_coverage'].transition_count(),
                   info['step_coverage'].crash_count(),
                   i[:8],
                   info['step_coverage'].transitions,
               ))


if __name__ == "__main__":
    main()
