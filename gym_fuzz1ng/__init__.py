import os

from gym.envs.registration import register


def afl_forkserver_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/afl-2.52b-mod/afl-2.52b/afl-forkserver',
    )


def libpng_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/libpng-1.6.34-mod/libpng_simple_fopen_afl',
    )


register(
    id='FuzzLibPNG-v0',
    entry_point='gym_fuzz1ng.envs:FuzzLibPNGEnv',
)


def simple_bits_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/simple_bits-mod/simple_bits_afl',
    )


register(
    id='FuzzSimpleBits-v0',
    entry_point='gym_fuzz1ng.envs:FuzzSimpleBitsEnv',
)


def simple_loop_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/simple_loop-mod/simple_loop_afl',
    )


register(
    id='FuzzSimpleLoop-v0',
    entry_point='gym_fuzz1ng.envs:FuzzSimpleLoopEnv',
)


def checksum_k_n_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/checksum_k_n-mod/checksum_k_n_afl',
    )


register(
    id='FuzzChecksum_2_2-v0',
    entry_point='gym_fuzz1ng.envs:FuzzChecksum_2_2Env',
)
register(
    id='FuzzChecksum_4_2-v0',
    entry_point='gym_fuzz1ng.envs:FuzzChecksum_4_2Env',
)
register(
    id='FuzzChecksum_8_2-v0',
    entry_point='gym_fuzz1ng.envs:FuzzChecksum_8_2Env',
)
register(
    id='FuzzChecksum_2_4-v0',
    entry_point='gym_fuzz1ng.envs:FuzzChecksum_2_4Env',
)
register(
    id='FuzzChecksum_4_4-v0',
    entry_point='gym_fuzz1ng.envs:FuzzChecksum_4_4Env',
)
register(
    id='FuzzChecksum_8_4-v0',
    entry_point='gym_fuzz1ng.envs:FuzzChecksum_8_4Env',
)
register(
    id='FuzzChecksum_2_8-v0',
    entry_point='gym_fuzz1ng.envs:FuzzChecksum_2_8Env',
)
register(
    id='FuzzChecksum_8_8-v0',
    entry_point='gym_fuzz1ng.envs:FuzzChecksum_8_8Env',
)
