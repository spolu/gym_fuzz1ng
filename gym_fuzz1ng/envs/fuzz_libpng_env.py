import gym_fuzz1ng
import gym_fuzz1ng.coverage as coverage

from gym_fuzz1ng.envs.fuzz_base_env import FuzzBaseEnv

class FuzzLibPNGEnv(FuzzBaseEnv):
    def __init__(self):
        self.target_path = gym_fuzz1ng.libpng_target_path()
        self.dict = coverage.Dictionary({
            'tokens': [
                b"\x89PNG\x0d\x0a\x1a\x0a",
                b"IDAT",
                b"IEND",
                b"IHDR",
                b"PLTE",
                b"bKGD",
                b"cHRM",
                b"fRAc",
                b"gAMA",
                b"gIFg",
                b"gIFt",
                b"gIFx",
                b"hIST",
                b"iCCP",
                b"iTXt",
                b"oFFs",
                b"pCAL",
                b"pHYs",
                b"sBIT",
                b"sCAL",
                b"sPLT",
                b"sRGB",
                b"sTER",
                b"tEXt",
                b"tIME",
                b"tRNS",
                b"zTXt"
            ],
            'bytes': True,
        })
        super(FuzzLibPNGEnv, self).__init__()
