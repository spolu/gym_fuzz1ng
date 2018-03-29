import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

from gym_fuzz1ng.envs.fuzz_base_env import FuzzBaseEnv

class FuzzSimpleBitsEnv(FuzzBaseEnv):
    def __init__(self):
        self.target_path = gym_fuzz1ng.simple_bits_target_path()
        self.dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzSimpleBitsEnv, self).__init__()
