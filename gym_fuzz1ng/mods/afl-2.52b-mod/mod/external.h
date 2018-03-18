/*
 * This has to do with external fuzzer link
 *
 */
#ifndef _HAVE_EXTERNAL_H
#define _HAVE_EXTERNAL_H

#include "types.h"
#include "config.h"

// WARNING: sync this with python models
#define MAX_INPUT_SIZE  (1 << 12)

#define MAX_EXTERNAL_CLIENTS	64

#define EXTERNAL_INPUT_QUEUE_NAME "/afl-external-input"
#define EXTERNAL_CLIENT_QUEUE_NAME "/afl-external-client-%08d"
#define EXTERNAL_CLIENT_SHM_NAME "/afl-external-client-%08d"

#pragma pack(1)
typedef struct ping_msg_hdr {
    u32 msgid;
    u32	type;
    u32 inputsize;
} PING_MSG_HDR;

typedef struct pong_msg_hdr {
    u32 msgid;
    u32 status;
    u32 size;   // always MAP_SIZE?
} PONG_MSG_HDR;



#pragma pack()


#define SHM_MAX_SIZE    	(int)MAX(MAP_SIZE, MAX_INPUT_SIZE)
#define MESSAGE_MAX_SIZE	(int)MAX(sizeof (PING_MSG_HDR), sizeof (PONG_MSG_HDR))

// defines for ping_msg_hdr->type
#define PING_NORMAL_MESSAGE 		0
#define PING_NEW_CLIENT_MESSAGE 	1
#define PING_DELETE_CLIENT_MESSAGE 	2


// defines for pong_msg_hdr->status
#define STATUS_CRASHED	0x80000000
#define STATUS_HANGED	0x40000000
#define STATUS_OK		0


#endif
