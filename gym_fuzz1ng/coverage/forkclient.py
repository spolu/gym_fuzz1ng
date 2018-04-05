#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from posix_ipc import *
import mmap
import struct
import random
import numpy
import traceback
import time

MAX_INPUT_SIZE = (2**14)
MAP_SIZE = (2**16)

_ping_struc_hdr = "<II"
_pong_struc = "<II"

# compute this only once
_ping_struc_hdr_size = struct.calcsize(_ping_struc_hdr)
_pong_struc_size = struct.calcsize(_pong_struc)

STATUS_CRASHED = 0x80000000
STATUS_HANGED  = 0x40000000
STATUS_ERROR   = 0x20000000

SHM_SIZE = max(
    MAP_SIZE + _pong_struc_size,
    MAX_INPUT_SIZE + _ping_struc_hdr_size,
)

SEM_PING_SIGNAL_NAME = "/afl-ping-signal"
SEM_PONG_SIGNAL_NAME = "/afl-pong-signal"
SHARED_MEM_NAME = "/afl-shared-mem"

def make_ping(msgid, input):
    """
    .--------------------.
    |    PING message    |
    |--------------------|
    | uint32 msgid       |
    | uint32 size        |
    | uint8  input[size] |
    '--------------------'
    """
    assert  (len(input) <= MAX_INPUT_SIZE)

    msg = struct.pack(
        _ping_struc_hdr + str(len(input)) + "s", msgid, len(input), input,
    )
    return msg

def get_pong(msg):
    """
    .------------------------.
    |      PONG message      |
    |------------------------|
    | uint32 msgid (same)    |
    | uint32 status          |
    | uint8  input[MAP_SIZE] |
    '------------------------'
    """
    (msgid, status) = struct.unpack(_pong_struc, msg[:_pong_struc_size])
    data = msg[_pong_struc_size:_pong_struc_size+MAP_SIZE]

    return (msgid, status, data)

def init_forkclient():
    shm = SharedMemory(SHARED_MEM_NAME)
    mm = mmap.mmap(shm.fd, 0)

    ping_sem = Semaphore(SEM_PING_SIGNAL_NAME)
    pong_sem = Semaphore(SEM_PONG_SIGNAL_NAME)

    return (mm, ping_sem, pong_sem)

if __name__ == '__main__':
    try:
        (mm, ping_sem, pong_sem) = init_forkclient()
    except:
        raise

    start = time.time()

    for i in range(10000):
        #print ("msg " + str(i))
        msgid_ping = random.randint(0, 100)
        ping_msg = make_ping(msgid_ping, b"hello\x00")

        mm.seek(0)
        mm.write(ping_msg)

        # tell server that a ping is ready
        ping_sem.release()

        # Wait for server to proceed with input
        # do anything while waiting for server...

        # Is there a pong ready?
        pong_sem.acquire()

        try:
            (msgid, status, data) = get_pong(mm[0:])
        except:
            print("Exception receiving a PONG!")
            pass

        #print("Received PONG with id: " + str(msgid));

    end = time.time()

    print ("Done {}".format(
        int(10000 / (end - start)),
    ))


"""
import posix_ipc
import mmap
import struct
import random
import numpy
import traceback
import signal
import os
import sys
import time
import tempfile
import subprocess
import threading
import gym_fuzz1ng

# TODO: make this better
MAX_INPUT_SIZE = (2**12)
MAP_SIZE = (2**16)

ping_struc_hdr = "<III"
pong_struc_hdr = "<III"

STATUS_CRASHED = 0x80000000
STATUS_HANGED = 0x40000000
STATUS_OK = 0

PING_NORMAL_MESSAGE = 0
PING_NEW_CLIENT_MESSAGE = 1
PING_DELETE_CLIENT_MESSAGE = 2

# compute this only once
pong_struc_hdr_size = struct.calcsize(pong_struc_hdr)
ping_struc_hdr_size = struct.calcsize(ping_struc_hdr)

SHM_MAX_SIZE = max(MAP_SIZE, MAX_INPUT_SIZE)
EXTERNAL_INPUT_QUEUE_NAME = "/afl-external-input"
EXTERNAL_CLIENT_QUEUE_NAME = "/afl-external-client-%08d"
EXTERNAL_CLIENT_SHM_NAME = "/afl-external-client-%08d"

_process = None
_target_path = None
_clients = {}
_lock = threading.Lock()

class ForkClient:
    def __init__(self, target_path, client_id, launch_afl_fuzz=True):
        global _process
        global _target_path
        global _clients

        self.client_id = client_id

        with _lock:
            if launch_afl_fuzz:
                if _process is None:
                    env = os.environ.copy()

                    if 'EXTERNAL_AFL_FUZZ' not in env:
                        print("Starting afl-fuzz in external mode")
                        afl_in = tempfile.mkdtemp(suffix='afl_in')
                        afl_out = tempfile.mkdtemp(suffix='afl_out')
                        dummy = open(os.path.join(afl_in, 'dummy'), "w")
                        dummy.write("foobar")
                        dummy.close()

                        env['AFL_NO_UI'] = '1'
                        FNULL = open(os.devnull, 'w')

                        cmd = [
                            gym_fuzz1ng.afl_fuzz_path(),
                            '-E',
                            '-i', afl_in,
                            '-o', afl_out,
                            '--',
                            target_path,
                            '@@',
                        ]
                        _process = subprocess.Popen(
                            cmd,
                            env=env,
                            stdout=FNULL,
                            stderr=subprocess.STDOUT,
                        )

                    _target_path = target_path
                else:
                    if target_path != _target_path:
                        raise Exception(
                            "Concurrent targets is not supported: {} {}".format(
                                target_path,
                                _target_Path,
                            ),
                        )
                _clients[self.client_id] = True

        # created by afl-mod
        self.mq_input = posix_ipc.MessageQueue(
            EXTERNAL_INPUT_QUEUE_NAME,
            flags = 0,
            max_messages = 100,
            max_message_size = ping_struc_hdr_size,
        )

        # created here
        try:
            self.mq_return = posix_ipc.MessageQueue(
                EXTERNAL_CLIENT_QUEUE_NAME % client_id,
                flags = posix_ipc.O_CREAT,
                max_messages = 10,
                max_message_size = (pong_struc_hdr_size),
            )
        except:
            print (
                "Exception while trying to create: /dev/mqueue" +
                EXTERNAL_CLIENT_QUEUE_NAME % client_id,
            )
            raise

        self.shm = posix_ipc.SharedMemory(
            EXTERNAL_CLIENT_SHM_NAME % client_id,
            flags = posix_ipc.O_CREAT,
            size = MAP_SIZE,
        )
        self.mm = mmap.mmap(self.shm.fd, MAP_SIZE)

        # send init signal to AFL (type init ping message)
        self.send_new()

    def __del__(self):
        global _clients
        self.send_delete()

        try:
            self.mm.close()
            self.shm.close_fd()
            #self.shm.unlink()
        except:
            raise

        try:
            self.mq_input.close()
            self.mq_return.unlink()
            self.mq_return.close()
        except:
            raise

        with _lock:
            if self.client_id in _clients:
                del _clients[self.client_id]
            if len(_clients.keys()) == 0 and _process is not None:
                _process.terminate()

    def send_new(self):
        self.send_ping(b"", PING_NEW_CLIENT_MESSAGE)

    def send_delete(self):
        self.send_ping(b"", PING_DELETE_CLIENT_MESSAGE)

    def send_ping(self, input, type=PING_NORMAL_MESSAGE):
        assert  (len(input) <= MAX_INPUT_SIZE)

        # write input to shm
        self.mm.seek(0)
        self.mm.write(input)
        self.mm.flush()

        # send message
        self.mq_input.send(
            struct.pack(ping_struc_hdr, self.client_id, type, len(input)),
        )

    def get_pong(self):
        (msg, _) = self.mq_return.receive()

        (msgid, status, size) = struct.unpack(
            pong_struc_hdr, msg[:pong_struc_hdr_size],
        )

        assert (size == MAP_SIZE)
        assert (self.client_id == msgid)

        # get data from shm
        self.mm.seek(0)
        data = self.mm.read(size)

        return (status, data)


def signal_handler(signal, frame):
    global _process

    if _process is not None:
        _process.terminate()

signal.signal(signal.SIGINT, signal_handler)
"""
