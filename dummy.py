import gym
import gym_fuzz1ng

def main():
    env = gym.make('FuzzLibPNG-v0')

    env.reset()

    inputs = [
        78, 89, 282,
        78, 282,
    ]
    for i in inputs:
        obs, reward, done = env.step(78)
        print("STEP {}: {} {}", i, reward, done)

if __name__ == "__main__":
    main()
