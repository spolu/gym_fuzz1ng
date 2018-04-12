import gym
import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage
import numpy as np

# import pdb; pdb.set_trace()

def main():
    env = gym.make('FuzzWordLibPNG-v0')

    env.reset()
    c = coverage.Coverage()

    inputs = [
        [1, 283] + [0] * 1022,
        [283] + [0] * 1023,
        [1, 283] + [0] * 1022,
    ]

    for i in inputs:
        obs, reward, done, info = env.step(np.array(i))
        c.add(info['step_coverage'])

        print("STEP: reward={} done={} step={}/{}/{} total={}/{}/{} sum={}/{}/{} action={}".format(
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
            print ("DONE!")


if __name__ == "__main__":
    main()
