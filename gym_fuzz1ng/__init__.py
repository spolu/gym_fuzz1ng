import os

from gym.envs.registration import register

register(
    id='FuzzLibPNG-v0',
    entry_point='gym_fuzz1ng.envs:FuzzLibPNGEnv',
)

def libpng_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_directory, '../build/mods/libpng-1.6.34-mod/libpng_simple_fopen_afl')
