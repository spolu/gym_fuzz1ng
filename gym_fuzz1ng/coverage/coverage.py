import numpy as np
import struct
import xxhash

from gym_fuzz1ng.coverage.forkclient import ForkClient
from gym_fuzz1ng.coverage.forkclient import STATUS_CRASHED

PATH_MAP_SIZE = 2**16
EDGE_MAP_SIZE = 2**8
IPC_DATA_MAGIC = 0xdeadbeef

'''
    UINT32  ipc_data_size;      // sanity checks...
    UINT32  status;             // status of the run
    UINT8   pathes[PATH_MAP_SIZE];
    UINT32  magic;              // sanity checks... TODO: get rid of it
'''
fmt_coverage = "=II" + str(PATH_MAP_SIZE) + "sI"


def coverage_struct_size():
    return struct.calcsize(fmt_coverage)


# extract structure from format, compute only once
IPC_DATA_SIZE = coverage_struct_size()


class Coverage:
    def __init__(self, shm=None, verbose=False):
        self.crashes = 0
        self.transitions = {}
        self.count_pathes = {}
        self.skip_pathes = {}
        self.verbose = verbose

        if shm is None:
            return

        # sanity check #1 (preload): nothing went wrong with System V ipc shm
        assert (len(shm) == IPC_DATA_SIZE)

        # load structure
        struct_coverage = struct.unpack_from(fmt_coverage, shm)
        coverage_ipc_data_size = struct_coverage[0]
        coverage_status = struct_coverage[1]
        coverage_pathes = struct_coverage[2]
        coverage_magic = struct_coverage[3]

        # sanity check #1 (postload): struct sizes (C / Python) match
        assert (coverage_ipc_data_size == IPC_DATA_SIZE)
        # sanity check #2 (postload): corruption of some kind
        assert (coverage_magic == IPC_DATA_MAGIC)

        if (coverage_status != 0):
            if coverage_status == STATUS_CRASHED:
                self.crashes = 1
        else:
            x_count = xxhash.xxh64()
            x_skip = xxhash.xxh64()

            for i in range(1, PATH_MAP_SIZE):
                if (coverage_pathes[i] != 0):
                    self.transitions[i] = coverage_pathes[i]
                    x_count.update(str(i) + '-' + str(coverage_pathes[i]))
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

        # create a fake structure and use IPC constructor...
        # very dirty, I know
        '''
            UINT32  ipc_data_size;     // sanity checks...
            UINT32  status;            // status of the run
            UINT8   pathes[PATH_MAP_SIZE];
            UINT32  magic;             // sanity checks... TODO: get rid of it.
        '''

        fake_shm = struct.pack(
            fmt_coverage, IPC_DATA_SIZE, status, data, IPC_DATA_MAGIC,
        )
        local_coverage = Coverage(fake_shm, self.verbose)

        return local_coverage
