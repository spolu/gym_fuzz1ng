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

            for i in range(0, PATH_MAP_SIZE):
                if (coverage_data[3*i+2] == 0):
                    break
                j = coverage_data[3*i+0] + coverage_data[3*i+1] * EDGE_MAP_SIZE
                self.transitions[j] = coverage_data[3*i+2]
                x_count.update(str(j) + '-' + str(self.transitions[j]))
                x_skip.update(str(j))

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

    def path_count(self):
        return len(self.count_pathes)

    def skip_path_count(self):
        return len(self.skip_pathes)

    def path_list(self):
        return [p for p in self.count_pathes]

    def skip_path_list(self):
        return [p for p in self.skip_pathes]


"""
AFL ENGINE
"""


class Afl:
    def __init__(self, target_path, args=[], verbose=False):
        global client_id
        self.verbose = verbose

        self.fc = ForkClient(target_path, args)

    def run(self, input_data):
        (status, data) = self.fc.run(input_data)

        local_coverage = Coverage(
            coverage_status=status, coverage_data=data, verbose=self.verbose,
        )

        return local_coverage
