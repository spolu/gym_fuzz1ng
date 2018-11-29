import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

from gym_fuzz1ng.envs.fuzz_base_env import FuzzBaseEnv


class FuzzChecksumBaseEnv(FuzzBaseEnv):
    def __init__(self):
        self.input_size = 72
        self.target_path = gym_fuzz1ng.checksum_k_n_target_path()
        self.dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzChecksumBaseEnv, self).__init__()


class FuzzChecksum_2_2Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['2', '2']
        super(FuzzChecksum_2_2Env, self).__init__()


class FuzzChecksum_4_2Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['4', '2']
        super(FuzzChecksum_4_2Env, self).__init__()


class FuzzChecksum_8_2Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['8', '2']
        super(FuzzChecksum_8_2Env, self).__init__()


class FuzzChecksum_2_4Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['2', '4']
        super(FuzzChecksum_2_4Env, self).__init__()


class FuzzChecksum_4_4Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['4', '4']
        super(FuzzChecksum_4_4Env, self).__init__()


class FuzzChecksum_8_4Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['8', '4']
        super(FuzzChecksum_8_4Env, self).__init__()


class FuzzChecksum_2_8Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['2', '8']
        super(FuzzChecksum_2_8Env, self).__init__()


class FuzzChecksum_4_8Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['4', '8']
        super(FuzzChecksum_4_8Env, self).__init__()


class FuzzChecksum_8_8Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['8', '8']
        super(FuzzChecksum_8_8Env, self).__init__()
