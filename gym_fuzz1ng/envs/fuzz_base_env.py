import gym

from gym import spaces

import gym_fuzz1ng.coverage as coverage


class FuzzBaseEnv(gym.Env):
    def __init__(self):
        # Classes that inherit FuzzBase must define before calling this
        # constructor:
        # - self.input_size
        # - self.dict
        # - self.target_path
        self.engine = coverage.Afl(
            self.target_path
        )
        self.observation_space = spaces.Box(
            0, 255, shape=(
                2, coverage.EDGE_MAP_SIZE, coverage.EDGE_MAP_SIZE
            ), dtype='int32',
        )
        self.action_space = spaces.Box(
            0, self.dict.eof(), shape=(self.input_size,), dtype='int32',
        )
        self.reset()

    def reset(self):
        self.total_coverage = coverage.Coverage()
        return coverage.Coverage().observation()

    def step(self, action):
        assert self.action_space.contains(action)

        reward = 0.0
        done = False

        input_data = b""

        for i in range(self.input_size):
            if int(action[i]) == self.dict.eof():
                break
            input_data += self.dict.bytes(int(action[i]))

        c = self.engine.run(input_data)

        old_path_count = self.total_coverage.skip_path_count()
        self.total_coverage.add(c)
        new_path_count = self.total_coverage.skip_path_count()

        if old_path_count == new_path_count:
            done = True

        reward = c.transition_count()

        if c.crash_count() > 0:
            print("CRASH {}".format(input_data))

        return c.observation(), reward, done, {
            "step_coverage": c,
            "total_coverage": self.total_coverage,
            "input_data": input_data,
        }

    def render(self, mode='human', close=False):
        pass

    def eof(self):
        return self.dict.eof()
