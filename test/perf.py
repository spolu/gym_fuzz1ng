import time
import gym
import gym_fuzz1ng

# import pdb; pdb.set_trace()


def main():
    env = gym.make('FuzzTokenLibPNG-v0')
    env.reset()

    start = time.time()

    print("Running sequential test...")
    for i in range(3000):
        obs, reward, done, info = env.step(0)
        env.reset()

    end = time.time()
    print("EPS {}".format(3000 / (end - start)))

if __name__ == "__main__":
    main()
