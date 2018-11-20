import numpy as np
import struct
import xxhash

from gym_fuzz1ng.coverage.forkclient import ForkClient
from gym_fuzz1ng.coverage.forkclient import STATUS_CRASHED

PATH_MAP_SIZE = 2**16
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
        self.pathes = {}
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
            x = xxhash.xxh64()

            for i in range(1, PATH_MAP_SIZE):
                if (coverage_pathes[i] != 0):
                    self.transitions[i] = coverage_pathes[i]
                    x.update(str(i))

            # print(">> COV: {}".format(self.transitions))

            self.pathes[x.digest()] = 1

    def clean(self):
        self.transitions = {}
        self.crashes = {}

    def transition_count(self):
        return len(self.transitions)

    def crash_count(self):
        return self.crashes

    def observation(self):
        v = np.zeros(PATH_MAP_SIZE)
        for i in self.transitions:
            v[i] = self.transitions[i]
        return v

    def add(self, coverage):
        for transition in coverage.transitions:
            if transition not in self.transitions:
                self.transitions[transition] = 0
            self.transitions[transition] += coverage.transitions[transition]
        for path in coverage.pathes:
            if path not in self.pathes:
                self.pathes[path] = 0
            self.pathes[path] += coverage.pathes[path]
        self.crashes += coverage.crashes

    def path_count(self):
        return len(self.pathes)


"""
AFL ENGINE
"""


class Afl:
    def __init__(self, target_path, verbose=False, launch_afl_forkserver=True):
        global client_id
        self.verbose = verbose

        self.fc = ForkClient(
            target_path, launch_afl_forkserver=launch_afl_forkserver,
        )

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
