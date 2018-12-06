/*
 * An adaptation of the code written by Nathan Voss <njvoss99@gmail.com> to
 * afl for use with gym_fuzz1ng.
 */
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define DATA_SIZE_MAX 0x00200000

uint32_t crc32_for_byte(uint32_t r) {
  for(int j = 0; j < 8; ++j)
    r = (r & 1? 0: (uint32_t)0xEDB88320L) ^ r >> 1;
  return r ^ (uint32_t)0xFF000000L;
}

typedef unsigned long accum_t;

void init_tables(uint32_t* table, uint32_t* wtable) {
  for(size_t i = 0; i < 0x100; ++i)
    table[i] = crc32_for_byte(i);
  for(size_t k = 0; k < sizeof(accum_t); ++k)
    for(size_t w, i = 0; i < 0x100; ++i) {
      for(size_t j = w = 0; j < sizeof(accum_t); ++j)
        w = table[(uint8_t)(j == k? w ^ i: w)] ^ w >> 8;
      wtable[(k << 8) + i] = w ^ (k? wtable[0]: 0);
    }
}

void crc32(const void* data, size_t n_bytes, uint32_t* crc) {
  static uint32_t table[0x100], wtable[0x100*sizeof(accum_t)];
  size_t n_accum = n_bytes/sizeof(accum_t);
  if(!*table)
    init_tables(table, wtable);
  for(size_t i = 0; i < n_accum; ++i) {
    accum_t a = *crc ^ ((accum_t*)data)[i];
    for(size_t j = *crc = 0; j < sizeof(accum_t); ++j)
      *crc ^= wtable[(j << 8) + (uint8_t)(a >> 8*j)];
  }
  for(size_t i = n_accum*sizeof(accum_t); i < n_bytes; ++i)
    *crc = table[(uint8_t)*crc ^ ((uint8_t*)data)[i]] ^ *crc >> 8;
}


void vulnerable(unsigned char* data_buf)
{
  uint32_t check = 0;
  uint32_t input = 0;

  crc32(data_buf, 8, &check);
  memcpy(&input, data_buf+8, sizeof input);

  if(input % (2<<8) == check % (2<<8)) {
    if(data_buf[0] == 0x01 && data_buf[1] == 0x02 &&
        data_buf[2] == 0x03 && data_buf[3] == 0x04 &&
        data_buf[4] == 0x05 && data_buf[5] == 0x06 &&
        data_buf[6] == 0x07 && data_buf[7] == 0x08)
    {
      // Crash if data[0..7] == "\x01\x02\x03\x04\x05\x06\x07\x08"
      asm ("xor %eax, %eax");
      asm ("xor %ecx, %ecx");
      asm ("movl	(%ecx),%eax");
    }
  }
}

int main(int argc, char **argv)
{
  int fd;
  struct stat st;

  char buffer[DATA_SIZE_MAX];

  if (argc < 2) {
    printf("usage: crc32_simple_bits <file_in>\n");
    exit(-2);
  }

  if ((fd = open(argv[1], O_RDONLY)) < 0) {
    printf("error opening file");
    exit(-1);
  }

  if (fstat (fd, &st) < 0) {
    printf("stating file");
    exit(-1);
  }

  if (read(fd, buffer, st.st_size) < 0) {
    printf("error reading file");
    exit(-1);
  }

  vulnerable(buffer);

  return 0;
}
