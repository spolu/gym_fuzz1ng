import gym

import numpy as np

from gym import error, spaces, utils
from gym.utils import seeding

import gym_fuzz1ng.coverage as coverage
import gym_fuzz1ng

MAX_INPUT_SIZE = 2**10

class FuzzBaseEnv(gym.Env):
    def __init__(self):
        # Classes that inherit FuzzBase must define self.dict and
        # self.target_path before calling this constructor.
        self.engine = coverage.Afl(
            self.target_path, launch_afl_fuzz=True,
        )
        self.observation_space = gym.spaces.Box(
            0, np.inf, shape=(2, coverage.PATH_MAP_SIZE), dtype='int32',
        )
        self.action_space = spaces.Discrete(self.dict.size())
        self.reset()

    def reset(self):
        self.input_data = b""
        self.total_coverage = coverage.Coverage()
        self.current_coverage = coverage.Coverage()

        return np.stack([
            self.current_coverage.observation(),
            self.total_coverage.observation(),
        ])

    def step(self, action):
        assert self.action_space.contains(action)

        reward = 0.0
        done = False
        eof = False

        if int(action) == self.dict.eof() or len(self.input_data) >= MAX_INPUT_SIZE:
            eof = True
            old_path_count = self.total_coverage.path_count()
            self.total_coverage.add(self.current_coverage)
            new_path_count = self.total_coverage.path_count()
            if old_path_count == new_path_count:
                done = True
        else:
            self.input_data += self.dict.bytes(int(action))

        c = self.engine.run(self.input_data)

        reward -= self.current_coverage.transition_count()
        self.current_coverage.add(c)
        reward += self.current_coverage.transition_count()

        if eof:
            self.input_data = b""
            self.current_coverage = coverage.Coverage()

        return np.stack([
            self.current_coverage.observation(),
            self.total_coverage.observation(),
        ]), reward, done, { "coverage": c }

    def render(self, mode='human', close=False):
        pass
