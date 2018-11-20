import gym
import gym_fuzz1ng.coverage as coverage
import numpy as np


def main():
    env = gym.make('FuzzWordSimpleBits-v0')

    env.reset()
    c = coverage.Coverage()

    inputs = [
        [1, 256] + [0] * 1022,
        [256] + [0] * 1023,
        [1, 1, 256] + [0] * 1021,
        [1, 1, 256] + [0] * 1021,

        [1, 1, 256] + [0] * 1021,
        [12, 256] + [0] * 1022,
        [12, 7, 256] + [0] * 1021,

        [1, 256] + [0] * 1022,
        [1, 2, 256] + [0] * 1021,
        [1, 2, 3, 256] + [0] * 1020,
        [1, 2, 3, 4, 256] + [0] * 1019,
        [1, 2, 3, 4, 5, 256] + [0] * 1018,
        [1, 1, 256] + [0] * 1021,

        [1, 1, 256] + [0] * 1021,
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 256] + [0] * 1013,
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 256] + [0] * 1012,
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 0, 256] + [0] * 1011,
        [1, 1, 256] + [0] * 1021,
    ]

    for i in inputs:
        obs, reward, done, info = env.step(np.array(i))
        c.add(info['step_coverage'])

        print(("STEP: reward={} done={} " +
               "step={}/{}/{} total={}/{}/{} " +
               "sum={}/{}/{} action={}").format(
                   reward, done,
                   info['step_coverage'].path_count(),
                   info['step_coverage'].transition_count(),
                   info['step_coverage'].crash_count(),
                   info['total_coverage'].path_count(),
                   info['total_coverage'].transition_count(),
                   info['total_coverage'].crash_count(),
                   c.path_count(),
                   c.transition_count(),
                   c.crash_count(),
                   i[:13],
               ))
        if done:
            env.reset()
            print("DONE!")


if __name__ == "__main__":
    main()
