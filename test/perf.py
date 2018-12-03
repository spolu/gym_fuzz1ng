import gym
import gym_fuzz1ng
import numpy as np
import time


def main():
    env = gym.make('FuzzSimpleLoop-v0')
    print("dict_size={} eof={}".format(env.dict_size(), env.eof()))

    i = [42, 255, env.dict.eof()-1] + [0] * 5

    start = time.time()
    run_count = 1000

    for _ in range(run_count):
        obs, reward, done, info = env.step(np.array(i))

    run_time = time.time() - start

    print("Finished: run_count={} exec_speed={} run_time={}".format(
        run_count,
        "%.2f" % (run_count / run_time),
        "%.2f" % (run_time),
    ))


if __name__ == "__main__":
    main()
