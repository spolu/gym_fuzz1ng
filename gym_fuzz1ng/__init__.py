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
    id='FuzzTokenLibPNG-v0',
    entry_point='gym_fuzz1ng.envs:FuzzTokenLibPNGEnv',
)
register(
    id='FuzzWordLibPNG-v0',
    entry_point='gym_fuzz1ng.envs:FuzzWordLibPNGEnv',
)


def simple_bits_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/simple_bits-mod/simple_bits_afl',
    )


register(
    id='FuzzTokenSimpleBits-v0',
    entry_point='gym_fuzz1ng.envs:FuzzTokenSimpleBitsEnv',
)
register(
    id='FuzzWordSimpleBits-v0',
    entry_point='gym_fuzz1ng.envs:FuzzWordSimpleBitsEnv',
)


def simple_loop_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/simple_loop-mod/simple_loop_afl',
    )


register(
    id='FuzzTokenSimpleLoop-v0',
    entry_point='gym_fuzz1ng.envs:FuzzTokenSimpleLoopEnv',
)
register(
    id='FuzzWordSimpleLoop-v0',
    entry_point='gym_fuzz1ng.envs:FuzzWordSimpleLoopEnv',
)
