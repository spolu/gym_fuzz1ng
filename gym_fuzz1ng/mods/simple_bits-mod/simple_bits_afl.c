/*
 * An adaptation of the code written by Nathan Voss <njvoss99@gmail.com> to
 * afl for use with gym_fuzz1ng.
 */
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define DATA_SIZE_MAX 0x00200000

void vulnerable(unsigned char* data_buf)
{
  printf("fooo %d %d\n", data_buf[0], data_buf[1]);

  if(data_buf[0] == 0x01 && data_buf[1] == 0x02 && data_buf[2] == 0x03 && data_buf[3] == 0x04 && data_buf[4] == 0x05)
  {
    // Cause an 'invalid read' crash if data[0..4] == "\x01\x02\x03\x04\x05"
    asm ("xor %eax, %eax");
    asm ("xor %ecx, %ecx");
    asm ("movl	(%ecx),%eax");
  }
  else if(data_buf[0] > 0x10 && data_buf[0] < 0x20 && data_buf[1] > data_buf[2])
  {
    // Cause an 'invalid read' crash if (0x10 < data[0] < 0x20) and data[1] > data[2]
    asm ("xor %eax, %eax");
    asm ("xor %ecx, %ecx");
    asm ("movl	(%ecx),%eax");
  }
  else if(data_buf[9] == 0x00 && data_buf[10] != 0x00 && data_buf[11] == 0x00)
  {
    // Cause a crash if data[10] is not zero, but [9] and [11] are zero
    asm ("xor %eax, %eax");
    asm ("xor %ecx, %ecx");
    asm ("movl	(%ecx),%eax");
  }
}

int main(int argc, char **argv)
{
  int fd;
  struct stat st;

  char buffer[DATA_SIZE_MAX];

  if (argc < 2) {
    printf("usage: simple_bits <file_in>\n");
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
