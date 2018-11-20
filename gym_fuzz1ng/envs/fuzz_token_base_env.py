import gym
import numpy as np

import gym_fuzz1ng.coverage as coverage


MAX_INPUT_SIZE = 1024


class FuzzTokenBaseEnv(gym.Env):
    def __init__(self):
        # Classes that inherit FuzzTokenBase must define before calling this
        # constructor:
        # - self.dict
        # - self.target_path
        self.engine = coverage.Afl(
            self.target_path, launch_afl_forkserver=True,
        )
        self.observation_space = gym.spaces.Box(
            0, np.inf, shape=(2, coverage.PATH_MAP_SIZE), dtype='int32',
        )
        self.action_space = gym.spaces.Discrete(self.dict.size())
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

        if int(action) == self.dict.eof() or \
                len(self.input_data) >= MAX_INPUT_SIZE:
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

        current_coverage = self.current_coverage

        if eof:
            self.input_data = b""
            self.current_coverage = coverage.Coverage()

        return np.stack([
            current_coverage.observation(),
            self.total_coverage.observation(),
        ]), reward, done, {
            "step_coverage": c,
            "current_coverage": current_coverage,
            "total_coverage": self.total_coverage,
        }

    def render(self, mode='human', close=False):
        pass
