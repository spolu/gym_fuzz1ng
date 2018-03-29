import gym
import gym_fuzz1ng

# import pdb; pdb.set_trace()

def main():
    env = gym.make('FuzzSimpleBits-v0')

    env.reset()

    coverage = gym_fuzz1ng.coverage.Coverage()

    inputs = [
        11, 12, 5, 255,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 10, 0, 255,
        1, 2, 3, 4, 5, 0, 255,
        0, 250, 282,
        0, 250, 1, 282,
        79, 282,
    ]
    for i in inputs:
        obs, reward, done, info = env.step(i)
        if i == 255:
            print("PATH_COUNT {}".format(info['coverage'].path_count()))
        print("STEP {}: {} {}".format(i, reward, done))

if __name__ == "__main__":
    main()
