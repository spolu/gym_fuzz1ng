import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

from gym_fuzz1ng.envs.fuzz_token_base_env import FuzzTokenBaseEnv
from gym_fuzz1ng.envs.fuzz_word_base_env import FuzzWordBaseEnv

class FuzzTokenSimpleBitsEnv(FuzzTokenBaseEnv):
    def __init__(self):
        self.target_path = gym_fuzz1ng.simple_bits_target_path()
        self.dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzTokenSimpleBitsEnv, self).__init__()

class FuzzWordSimpleBitsEnv(FuzzWordBaseEnv):
    def __init__(self):
        self.target_path = gym_fuzz1ng.simple_bits_target_path()
        self.dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzWordSimpleBitsEnv, self).__init__()
