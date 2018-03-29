import gym
import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

# import pdb; pdb.set_trace()

def main():
    env = gym.make('FuzzSimpleBits-v0')

    env.reset()
    c = coverage.Coverage()

    inputs = [
        11, 12, 5, 255,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 10, 0, 255,
        1, 2, 3, 4, 5, 0, 255,
        0, 250, 255,
        0, 250, 1, 255,
        79, 255,
    ]
    for i in inputs:
        obs, reward, done, info = env.step(i)
        c.add(info['step_coverage'])

        print("STEP {}: {} {}".format(i, reward, done))
        if i == 255:
            print("COUNTS {}/{} {}/{}".format(
                info['step_coverage'].path_count(),
                info['step_coverage'].transition_count(),
                c.path_count(),
                c.transition_count(),
            ))

if __name__ == "__main__":
    main()
