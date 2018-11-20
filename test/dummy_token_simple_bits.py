import gym
import gym_fuzz1ng.coverage as coverage


def main():
    env = gym.make('FuzzTokenSimpleBits-v0')

    env.reset()
    c = coverage.Coverage()

    inputs = [
        1, 1, 256,
        1, 1, 256,

        1, 1, 256,
        12, 256,
        12, 7, 256,
        1, 1, 256,

        1, 1, 256,
        1, 2, 3, 256,
        1, 2, 3, 4, 256,
        1, 2, 3, 4, 5, 256,
        1, 1, 256,

        1, 1, 256,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 256,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 256,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 0, 256,
        1, 1, 256,
    ]
    for i in inputs:
        obs, reward, done, info = env.step(i)
        c.add(info['step_coverage'])

        print(("STEP: reward={} done={} " +
               "step={}/{}/{} current={}/{}/{} " +
               "total={}/{}/{} sum={}/{}/{} action={}").format(
                   reward, done,
                   info['step_coverage'].path_count(),
                   info['step_coverage'].transition_count(),
                   info['step_coverage'].crash_count(),
                   info['current_coverage'].path_count(),
                   info['current_coverage'].transition_count(),
                   info['current_coverage'].crash_count(),
                   info['total_coverage'].path_count(),
                   info['total_coverage'].transition_count(),
                   info['total_coverage'].crash_count(),
                   c.path_count(),
                   c.transition_count(),
                   c.crash_count(),
                   i,
               ))
        if done:
            env.reset()
            print("DONE!")


if __name__ == "__main__":
    main()
