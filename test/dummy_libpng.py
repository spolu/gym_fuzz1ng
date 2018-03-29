import gym
import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

# import pdb; pdb.set_trace()

def main():
    env = gym.make('FuzzLibPNG-v0')

    env.reset()
    c = coverage.Coverage()

    inputs = [
        78, 89, 282,
        0, 250, 282,
        0, 250, 1, 282,
        79, 282,
    ]
    for i in inputs:
        obs, reward, done, info = env.step(i)
        c.add(info['step_coverage'])
        print("STEP {}: {} {}".format(i, reward, done))
        if i == 282:
            print("COUNTS {}/{} {}/{}".format(
                info['step_coverage'].path_count(),
                info['step_coverage'].transition_count(),
                c.path_count(),
                c.transition_count(),
            ))

if __name__ == "__main__":
    main()
