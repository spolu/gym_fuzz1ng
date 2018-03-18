import os
import struct
import subprocess
import tempfile
import signal

import sysv_ipc
import posix_ipc

import numpy as np

import xxhash

from coverage.forkclient import ForkClient

PATH_MAP_SIZE = 2**16
IPC_DATA_MAGIC = 0xdeadbeef

'''
    UINT32  ipc_data_size;      // sanity checks...

    UINT64  instruction_RVA;    // RVA of last instruction
    UINT64  lastblock_RVA;      // RVA of first instruction of last block
    UINT64  crash_info;         // used as a boolean

    UINT8   pathes[PATH_MAP_SIZE];
    UINT32  blockCount;         // extra indicator

    UINT32  magic;              // sanity checks... TODO: get rid of it
'''
fmt_coverage = "=IQQQ" + str(PATH_MAP_SIZE) + "sII"

def coverage_struct_size():
    return struct.calcsize(fmt_coverage)

# extract structure from format, compute only once
IPC_DATA_SIZE = coverage_struct_size()

class Coverage:
    def __init__(self, shm=None, verbose=False):
        self.last_block = 0
        self.instruction = None
        self.transitions = {}
        self.crashes = {}
        self.pathes = {}
        self.verbose = verbose

        if shm == None:
            return

        # sanity check #1 (preload): nothing went wrong with System V ipc shm
        assert (len(shm) == IPC_DATA_SIZE)

        # load structure
        struct_coverage = struct.unpack_from(fmt_coverage, shm)
        coverage_ipc_data_size =    struct_coverage[0]
        coverage_instruction_RVA =  struct_coverage[1]
        coverage_lastblock_RVA =    struct_coverage[2]
        coverage_crash_offset =     struct_coverage[3]
        coverage_pathes =           struct_coverage[4]
        coverage_blockCount =       struct_coverage[5]
        coverage_magic =            struct_coverage[6]

        # sanity check #2 (postload): struct sizes (C / Python) match
        assert (coverage_ipc_data_size == IPC_DATA_SIZE)

        # sanity check #3 (postload): corruption of some kind
        assert (coverage_magic == IPC_DATA_MAGIC)

        x = xxhash.xxh64()

        self.instruction = coverage_instruction_RVA
        for i in range (1, PATH_MAP_SIZE):
            if (coverage_pathes[i] != 0):
                self.transitions[i] = coverage_pathes[i]
                x.update(str(i))

        self.pathes[x.digest()] = 1

        if (coverage_crash_offset != 0):
            self.crashes[coverage_instruction_RVA] = 1
            self.transitions = {}
            self.pathes = {}

    def code(self, address):
        self.instruction = address
        """
            def crash(self):
                address = self.instruction
                if address in self.crashes:
                    self.crashes[address] += 1
                else:
                    self.crashes[address] = 1
        """

    def block(self, address):
        transition = str(hex(self.last_block)) + " -> " + str(hex(address))
        if self.verbose:
            print("New transition " + transition)
        if transition in self.transitions:
            self.transitions[transition] += 1
        else:
            self.transitions[transition] = 1
        self.last_block = address

    def clean(self):
        self.last_block = None
        self.instruction = None
        self.transitions = {}
        self.crashes = {}

    def transition_count(self):
        return len(self.transitions)

    def crash_count(self):
        return len(self.crashes)

    def observation(self):
        v = np.zeros(PATH_MAP_SIZE)
        for i in self.transitions:
            v[i] = self.transitions[i]
        return v

    def add(self, coverage):
        if coverage.crash_count() == 0:
            for transition in coverage.transitions:
                if transition not in self.transitions:
                    self.transitions[transition] = 0
                self.transitions[transition] += coverage.transitions[transition]
            for path in coverage.pathes:
                if path not in self.pathes:
                    self.pathes[path] = 0
                self.pathes[path] += coverage.pathes[path]
        else:
            for address in coverage.crashes:
                if address not in self.crashes:
                    self.crashes[address] = 0
                self.crashes[address] += coverage.crashes[address]

    def path_count(self):
        return len(self.pathes)

"""
AFL ENGINE
"""

client_id = 0
afl_running = False

class Afl:
    def __init__(self, target_path, verbose=False):
        global client_id
        self.verbose = verbose
        self.client_id = client_id
        client_id += 1

        # creates everything
        try:
            self.fc = ForkClient(target_path, client_id)

        except:
            print ( " ***\n"
                    " ***   We couldn't connect to AFL forkserver \n"
                    " ***\n"
                    " ***   You have to run something like this prior to using this engine: \n"
                    " ***      ./afl-fuzz -E -i <SOMETHING> -o <SOMETHING ELSE> -- <target_path> @@ \n"
                    " ***\n"
                    " ***\n")
            raise

    def run(self, input_data):
        #print ("msg " + str(i))
        self.fc.send_ping(input_data)

        try:
            (status, data) = self.fc.get_pong()
        except:
            print("Exception receiving a PONG!")
            raise

        # create a fake structure and use IPC constructor...
        # very dirty, I know
        '''
            UINT32  ipc_data_size;      // sanity checks...

            UINT64  instruction_RVA;    // RVA of last instruction
            UINT64  lastblock_RVA;      // RVA of first instruction of last block
            UINT64  crash_info;         // used as a boolean

            UINT8   pathes[PATH_MAP_SIZE];
            UINT32  blockCount;         // extra indicator

            UINT32  magic;              // sanity checks... TODO: get rid of it
        '''

        # STATUS_OK means that bitmap is reliable
        # TODO: do something clean, this is horrible fix
        if status == STATUS_OK:
            crash_info = 0
        else:
            crash_info = 1

        fake_shm = struct.pack(fmt_coverage, IPC_DATA_SIZE, 0, 0, crash_info, data, 0, IPC_DATA_MAGIC)
        local_coverage = Coverage(fake_shm, self.verbose)

        return local_coverage
