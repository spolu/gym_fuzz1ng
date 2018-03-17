#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from multiprocessing import Process, Pipe

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

class ForkClient:
    def send_new(self):
        self.send_ping(b"", PING_NEW_CLIENT_MESSAGE)

        def send_delete(self):
            self.send_ping(b"", PING_DELETE_CLIENT_MESSAGE)


        def send_ping(self, input, type=PING_NORMAL_MESSAGE):
            """
	                                 .--------------------.
	                                 |    PING message    |
	      |==|=====|                 |--------------------|
	      |  |     |---------------->| uint32 msgid       |-------------.
	      |  |     |                 | uint32 type        |             |
	      |  |     |		 | uint32 size        |             |
	      |  |     |                 '--------------------'             |
	      |  |     |                                                    |
	      |  |====°|                                                    |
	      |__|_____|                                                    |
	   External fuzzer                                                  |
	   (python3 daemon)                                                 |
            """
            assert  (len(input) <= MAX_INPUT_SIZE)

            # write input to shm
            self.mm.seek(0)
            self.mm.write(input)
            self.mm.flush()

            # send message
            self.mq_input.send(struct.pack(ping_struc_hdr, self.client_id, type, len(input)))

        def get_pong(self):
            """
	           ^
	           |               .----------------------.             ________
	           |               |     PONG message     |            |==|=====|
	           |               |----------------------|            |  |     |
	           |               | uint32 msgid (same)  |            |  |     |
	           '---------------| uint32 status        |<-----------|  |     |
	                           | uint32 size          |            |  |     |
                                   '----------------------'            |  |====°|
                                                                       |__|_____|
            """
            (msg, _) = self.mq_return.receive()

            (msgid, status, size) = struct.unpack(pong_struc_hdr, msg[:pong_struc_hdr_size])

            assert (size == MAP_SIZE)

            assert (self.client_id == msgid)

            # get data from shm
            self.mm.seek(0)
            data = self.mm.read(size)

            return (status, data)

        def __init__(self, client_id):
            self.client_id = client_id

            # created by afl-mod
            self.mq_input = posix_ipc.MessageQueue(EXTERNAL_INPUT_QUEUE_NAME, flags = 0, max_messages = 100, max_message_size = ping_struc_hdr_size)

            # created here
            try:
                self.mq_return = posix_ipc.MessageQueue(EXTERNAL_CLIENT_QUEUE_NAME % client_id, flags = posix_ipc.O_CREAT, max_messages = 10, max_message_size = (pong_struc_hdr_size))
            except:
                print ("Exception while trying to create: /dev/mqueue" + EXTERNAL_CLIENT_QUEUE_NAME % client_id)
                raise

            self.shm = posix_ipc.SharedMemory(EXTERNAL_CLIENT_SHM_NAME % client_id, flags = posix_ipc.O_CREAT, size = MAP_SIZE)
            self.mm = mmap.mmap(self.shm.fd, MAP_SIZE)

            # send init signal to AFL (type init ping message)
            self.send_new()

        def __del__(self):
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


def worker(client_id):
    import resource
    try:
        fc = ForkClient(client_id)
    except:
        raise

    while True:
        #print ("msg " + str(i))
        fc.send_ping(b"hello\x00")

        # simulate some computation
        time.sleep(.0001)

        try:
            (status, data) = fc.get_pong()
        except:
            print("Exception receiving a PONG!")
            raise

        if data != bytes(MAP_SIZE):
            print("NOT NULL")
            for i in data:
                if data[i] != 0:
                    print (str(data[i]) + "    " + str(i) + " / " + str(MAP_SIZE))
                #print(data[:10])
                #print("Received PONG with id: " + str(msgid));

        print ("Done")

# "clean" exit
def signal_handler(signal, frame):
    print ("Bye-bye")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    try:
        nb_proc = int(sys.argv[1], 10)
    except:
        print ("Args: " + sys.argv[0] + " <Nb processes>")

        jobs = []
        for i in range(nb_proc):
            print ("Starting " + str(i))
            p = Process(target=worker, args=(i,))
            jobs.append(p)
            p.start()
            time.sleep(.2)
