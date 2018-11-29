import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

from gym_fuzz1ng.envs.fuzz_base_env import FuzzBaseEnv


class FuzzChecksumBaseEnv(FuzzBaseEnv):
    def __init__(self):
        self.input_size = 16
        self.target_path = gym_fuzz1ng.checksum_k_n_target_path()
        self.dict = coverage.Dictionary({
            'tokens': [],
            'bytes': True,
        })
        super(FuzzChecksumBaseEnv, self).__init__()


class FuzzChecksum_1_2Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['1', '2']
        super(FuzzChecksum_1_2Env, self).__init__()


class FuzzChecksum_2_2Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['2', '2']
        super(FuzzChecksum_2_2Env, self).__init__()


class FuzzChecksum_3_2Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['3', '2']
        super(FuzzChecksum_3_2Env, self).__init__()


class FuzzChecksum_4_2Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['4', '2']
        super(FuzzChecksum_4_2Env, self).__init__()


class FuzzChecksum_1_3Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['1', '3']
        super(FuzzChecksum_1_3Env, self).__init__()


class FuzzChecksum_2_3Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['2', '3']
        super(FuzzChecksum_2_3Env, self).__init__()


class FuzzChecksum_3_3Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['3', '3']
        super(FuzzChecksum_3_3Env, self).__init__()


class FuzzChecksum_4_3Env(FuzzChecksumBaseEnv):
    def __init__(self):
        self.args = ['4', '3']
        super(FuzzChecksum_4_3Env, self).__init__()
