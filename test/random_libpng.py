import random
import gym
import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

# import pdb; pdb.set_trace()

def main():
    random.seed(0)
    env = gym.make('FuzzLibPNG-v0')

    env.reset()
    c = coverage.Coverage()

    print("ACTION SIZE: {}".format(env.action_space))

    for i in range(1000):
        nxt = random.randint(0, env.action_space.n-1)
        obs, reward, done, info = env.step(nxt)

        print("STEP: reward={} done={} step={}/{}/{} current={}/{}/{} total={}/{}/{} action={}".format(
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
            nxt,
        ))

        if done:
            env.reset()
            print ("DONE!")

if __name__ == "__main__":
    main()
