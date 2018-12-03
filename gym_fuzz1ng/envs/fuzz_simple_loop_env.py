import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

from gym_fuzz1ng.envs.fuzz_base_env import FuzzBaseEnv


class FuzzSimpleLoopEnv(FuzzBaseEnv):
    def __init__(self):
        self._input_size = 8
        self._target_path = gym_fuzz1ng.simple_loop_target_path()
        self._args = []
        self._dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzSimpleLoopEnv, self).__init__()
