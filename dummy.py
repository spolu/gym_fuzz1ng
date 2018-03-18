import gym
import gym_fuzz1ng

# import pdb; pdb.set_trace()

def main():
    env = gym.make('FuzzLibPNG-v0')

    env.reset()

    inputs = [
        78, 89, 282,
        0, 1, 282,
        78, 282,
    ]
    for i in inputs:
        obs, reward, done, info = env.step(i)
        print("STEP {}: {} {}".format(i, reward, done))

if __name__ == "__main__":
    main()
