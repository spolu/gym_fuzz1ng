import gym
import gym_fuzz1ng  # noqa F401
import numpy as np


def main():
    env = gym.make('FuzzChecksum_2_2-v0')
    print("dict_size={} eof={}".format(env.dict.size(), env.eof()))

    env.reset()

    inputs = [
        [0, 0, 1, 1, 0, 0] + [0] * 10,
        [2, 1, 1, 3, 0, 0] + [0] * 10,
        [2, 0, 0, 3, 2, 1] + [0] * 10,
        [2, 1, 1, 3, 2, 1] + [0] * 10,
        [144, 200, 200, 150, 150, 150] + [0] * 10,
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
