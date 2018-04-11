import gym

import numpy as np

from gym import error, spaces, utils
from gym.utils import seeding

import gym_fuzz1ng.coverage as coverage
import gym_fuzz1ng

INPUT_SIZE = 1024

class FuzzWordBaseEnv(gym.Env):
    def __init__(self):
        # Classes that inherit FuzzWordBase must define before calling this
        # constructor:
        # - self.dict
        # - self.target_path
        self.engine = coverage.Afl(
            self.target_path, launch_afl_forkserver=True,
        )
        self.observation_space = gym.spaces.Box(
            0, np.inf, shape=(2, coverage.PATH_MAP_SIZE), dtype='int32',
        )
        self.action_space = gym.spaces.Box(
            0, self.dict.size(), shape=(INPUT_SIZE,), dtype='int32',
        )
        self.reset()

    def reset(self):
        self.total_coverage = coverage.Coverage()

        return np.stack([
            self.total_coverage.observation(),
            coverage.Coverage().observation(),
        ])

    def step(self, action):
        assert self.action_space.contains(action)

        reward = 0.0
        done = False
        eof = False

        input_data = b""

        for i in range(INPUT_SIZE):
            if int(action[i]) == self.dict.eof():
                break
            input_data += self.dict.bytes(int(action[i]))

        c = self.engine.run(input_data)

        old_path_count = self.total_coverage.path_count()
        self.total_coverage.add(c)
        new_path_count = self.total_coverage.path_count()

        if old_path_count == new_path_count:
            done = True

        reward = c.transition_count()

        return np.stack([
            self.total_coverage.observation(),
            c.observation(),
        ]), reward, done, {
            "step_coverage": c,
            "total_coverage": self.total_coverage,
        }

    def render(self, mode='human', close=False):
        pass
