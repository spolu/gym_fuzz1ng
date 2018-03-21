import time
import gym
import gym_fuzz1ng

from multiprocessing import Process, Pipe

# import pdb; pdb.set_trace()

def worker(remote, parent_remote):
    parent_remote.close()

    env = gym.make('FuzzLibPNG-v0')
    env.reset()

    while True:
        action = remote.recv()
        obs, reward, done, info = env.step(action)
        env.reset()
        remote.send(obs)


def main():
    env = gym.make('FuzzLibPNG-v0')
    env.reset()

    start = time.time()

    print("Running sequential test...")
    for i in range(300):
        obs, reward, done, info = env.step(0)
        env.reset()

    end = time.time()
    print("EPS {}".format(300 / (end - start)))

    process_count = 16
    remotes, work_remotes = zip(*[Pipe() for _ in range(process_count)])

    ps = [Process(target=worker, args=(work_remote, remote))
        for (work_remote, remote, client_id) in zip(work_remotes, remotes, range(process_count))]
    for p in ps:
        p.daemon = True # if the main process crashes, we should not cause things to hang
        p.start()
    for remote in work_remotes:
        remote.close()

    start = time.time()

    print("Running parallel test...")
    for i in range(10):
        for i in range(process_count):
            remote = remotes[i]
            remote.send(0)
        obs = [remote.recv() for remote in remotes]

    end = time.time()
    print("EPS {}".format(10*process_count / (end - start)))

if __name__ == "__main__":
    main()
