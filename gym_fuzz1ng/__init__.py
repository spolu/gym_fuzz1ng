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
