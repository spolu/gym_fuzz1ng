import gym

from gym import error, spaces, utils
from gym.utils import seeding

from coverage import Coverage
import gym_fuzz1ng

class FuzzLibPNGEnv(gym.Env):
    def __init__(self):
        c = Coverage()
        print('>>>' + gym_fuzz1ng.get_libpng_target_path())
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass
