/*
 * This has to do with external fuzzer link
 *
 */
#ifndef _HAVE_EXTERNAL_H
#define _HAVE_EXTERNAL_H

#include "types.h"
#include "config.h"

#define MAX_INPUT_SIZE  (1 << 12)

#define SEM_PING_SIGNAL_NAME "/afl-ping-signal"
#define SEM_PONG_SIGNAL_NAME "/afl-pong-signal"
#define SHARED_MEM_NAME "/afl-shared-mem"

#pragma pack(1)
typedef struct ping_msg_hdr {
    u32 msgid;
    u32 inputsize;
} PING_MSG_HDR;

typedef struct pong_msg {
    u32 msgid;
    u32 status;
    u8  trace_bits[MAP_SIZE];
} PONG_MSG;

#pragma pack()

#define SHM_SIZE MAX(sizeof(PONG_MSG), MAX_INPUT_SIZE + sizeof(PING_MSG_HDR))

// defines for pong_msg_hdr->status
#define STATUS_CRASHED	0x80000000
#define STATUS_HANGED	0x40000000
#define STATUS_ERROR    0x20000000
#define STATUS_OK		0

#endif
