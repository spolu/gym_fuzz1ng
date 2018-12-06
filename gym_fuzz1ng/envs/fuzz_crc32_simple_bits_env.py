import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

from gym_fuzz1ng.envs.fuzz_base_env import FuzzBaseEnv


class FuzzCRC32SimpleBitsEnv(FuzzBaseEnv):
    def __init__(self):
        self._input_size = 12
        self._target_path = gym_fuzz1ng.crc32_simple_bits_target_path()
        self._args = []
        self._dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzCRC32SimpleBitsEnv, self).__init__()
