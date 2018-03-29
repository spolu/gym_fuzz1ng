import gym
import gym_fuzz1ng

# import pdb; pdb.set_trace()

def main():
    env = gym.make('FuzzLibPNG-v0')

    env.reset()

    inputs = [
        78, 89, 282,
        0, 250, 282,
        0, 250, 1, 282,
        79, 282,
    ]
    for i in inputs:
        obs, reward, done, info = env.step(i)
        if i == 282:
            print("PATH_COUNT {}".format(info['coverage'].path_count()))
        print("STEP {}: {} {}".format(i, reward, done))

if __name__ == "__main__":
    main()
