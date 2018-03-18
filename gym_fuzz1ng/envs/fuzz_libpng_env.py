import gym

import numpy as np

from gym import error, spaces, utils
from gym.utils import seeding

import coverage
import gym_fuzz1ng

MAX_INPUT_SIZE = 2**10

_dict = coverage.Dictionary({
    'tokens': [
        b"\x89PNG\x0d\x0a\x1a\x0a",
        b"IDAT",
        b"IEND",
        b"IHDR",
        b"PLTE",
        b"bKGD",
        b"cHRM",
        b"fRAc",
        b"gAMA",
        b"gIFg",
        b"gIFt",
        b"gIFx",
        b"hIST",
        b"iCCP",
        b"iTXt",
        b"oFFs",
        b"pCAL",
        b"pHYs",
        b"sBIT",
        b"sCAL",
        b"sPLT",
        b"sRGB",
        b"sTER",
        b"tEXt",
        b"tIME",
        b"tRNS",
        b"zTXt"
    ],
    'bytes': True,
})

class FuzzLibPNGEnv(gym.Env):
    def __init__(self):
        self.engine = coverage.Afl(
            gym_fuzz1ng.libpng_target_path(),
        )
        self.observation_space = gym.spaces.Box(
            0, np.inf, shape=(2, coverage.PATH_MAP_SIZE), dtype='float32',
        )
        self.action_space = spaces.Discrete(_dict.size())
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

        if int(action) == _dict.eof() or len(self.input_data) >= MAX_INPUT_SIZE:
            eof = True
            old_path_count = self.total_coverage.path_count()
            self.total_coverage.add(self.current_coverage)
            new_path_count = self.total_coverage.path_count()
            if old_path_count == new_path_count:
                done = True
        else:
            self.input_data += _dict.bytes(int(action))

        coverage = self.engine.run(self.input_data)

        reward -= self.current_coverage.transition_count()
        self.current_coverage.add(coverage)
        reward += self.current_coverage.transition_count()

        if eof:
            self.input_data = b""
            self.current_coverage = coverage.Coverage()

        return np.stack([
            self.current_coverage.observation(),
            self.total_coverage.observation(),
        ]), reward, done, {}

    def render(self, mode='human', close=False):
        pass
