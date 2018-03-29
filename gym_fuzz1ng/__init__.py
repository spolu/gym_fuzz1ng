import os

from gym.envs.registration import register

def afl_fuzz_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_directory, 'mods/afl-2.52b-mod/afl-2.52b/afl-fuzz')

register(
    id='FuzzLibPNG-v0',
    entry_point='gym_fuzz1ng.envs:FuzzLibPNGEnv',
)
def libpng_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_directory, 'mods/libpng-1.6.34-mod/libpng_simple_fopen_afl')

register(
    id='FuzzSimpleBits-v0',
    entry_point='gym_fuzz1ng.envs:FuzzSimpleBitsEnv',
)
def simple_bits_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_directory, 'mods/simple_bits-mod/simple_bits_afl')
