import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

from gym_fuzz1ng.envs.fuzz_token_base_env import FuzzTokenBaseEnv
from gym_fuzz1ng.envs.fuzz_word_base_env import FuzzWordBaseEnv


class FuzzTokenSimpleLoopEnv(FuzzTokenBaseEnv):
    def __init__(self):
        self.max_input_size = 8
        self.target_path = gym_fuzz1ng.simple_loop_target_path()
        self.dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzTokenSimpleLoopEnv, self).__init__()


class FuzzWordSimpleLoopEnv(FuzzWordBaseEnv):
    def __init__(self):
        self.max_input_size = 8
        self.target_path = gym_fuzz1ng.simple_loop_target_path()
        self.dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzWordSimpleLoopEnv, self).__init__()
