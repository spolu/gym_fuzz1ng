import numpy as np
# import struct
import xxhash

from gym_fuzz1ng.coverage.forkclient import ForkClient
from gym_fuzz1ng.coverage.forkclient import STATUS_CRASHED

PATH_MAP_SIZE = 2**16
EDGE_MAP_SIZE = 2**8


class Coverage:
    def __init__(
            self, coverage_status=None, coverage_data=None, verbose=False,
    ):
        self.crashes = 0
        self.transitions = {}
        self.count_pathes = {}
        self.skip_pathes = {}
        self.verbose = verbose

        if coverage_status is None:
            return
        assert coverage_data is not None

        if (coverage_status != 0):
            if coverage_status == STATUS_CRASHED:
                self.crashes = 1
        else:
            x_count = xxhash.xxh64()
            x_skip = xxhash.xxh64()

            # for i in range(1, int(PATH_MAP_SIZE/8)):
            #     q = struct.unpack("<Q", coverage_data[i:i+8])[0]
            #     if q != 0:
            #         for j in range(8):
            #             k = 8*i+j
            #             self.transitions[k] = coverage_data[k]
            #             x_count.update(str(k) + '-' + str(coverage_data[k]))
            #             x_skip.update(str(k))

            for i in range(1, PATH_MAP_SIZE):
                if (coverage_data[i] != 0):
                    self.transitions[i] = coverage_data[i]
                    x_count.update(str(i) + '-' + str(coverage_data[i]))
                    x_skip.update(str(i))

            # print(">> COV: {}".format(self.transitions))

            self.count_pathes[x_count.digest()] = 1
            self.skip_pathes[x_skip.digest()] = 1

    def clean(self):
        self.transitions = {}
        self.count_pathes = {}
        self.skip_pathes = {}
        self.crashes = 0

    def transition_count(self):
        return len(self.transitions)

    def crash_count(self):
        return self.crashes

    def observation(self):
        v = np.zeros((EDGE_MAP_SIZE, EDGE_MAP_SIZE))
        for i in self.transitions:
            v[i % EDGE_MAP_SIZE][int(i / EDGE_MAP_SIZE)] = self.transitions[i]
        return v

    def add(self, coverage):
        for transition in coverage.transitions:
            if transition not in self.transitions:
                self.transitions[transition] = 0
            self.transitions[transition] += coverage.transitions[transition]
        for path in coverage.count_pathes:
            if path not in self.count_pathes:
                self.count_pathes[path] = 0
            self.count_pathes[path] += coverage.count_pathes[path]
        for path in coverage.skip_pathes:
            if path not in self.skip_pathes:
                self.skip_pathes[path] = 0
            self.skip_pathes[path] += coverage.skip_pathes[path]
        self.crashes += coverage.crashes

    def count_path_count(self):
        return len(self.count_pathes)

    def skip_path_count(self):
        return len(self.skip_pathes)

    def count_path_list(self):
        return [p for p in self.count_pathes]

    def skip_path_list(self):
        return [p for p in self.skip_pathes]


"""
AFL ENGINE
"""


class Afl:
    def __init__(self, target_path, verbose=False):
        global client_id
        self.verbose = verbose

        self.fc = ForkClient(target_path)

    def run(self, input_data):
        (status, data) = self.fc.run(input_data)

        local_coverage = Coverage(
            coverage_status=status, coverage_data=data, verbose=self.verbose,
        )

        return local_coverage
