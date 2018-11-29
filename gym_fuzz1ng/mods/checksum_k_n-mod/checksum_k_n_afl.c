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
#include <time.h>

#define DATA_SIZE_MAX 0x00200000



unsigned char chksum8(const unsigned char *buffer, unsigned int base, size_t len)
{
  unsigned int sum;
  for ( sum = base ; len != 0 ; len-- )
    sum += *(buffer++);
  return (unsigned char)sum;
}

void vulnerable(unsigned char* buffer, int chksum_count, int chksum_length)
{
  int success_count = 0;
  int magic_value = 0;
  int base = 42;

  for(int i = 0; i < chksum_count; i++) {
    int pos = i * (chksum_length + 1);
    if(buffer[pos] == chksum8(buffer+(pos+1), base+i, chksum_length)) {
      success_count += 1;

      if(i == 0) {
        magic_value += 1;
      }
      if(i == 1) {
        magic_value += 3;
      }
      if(i == 2) {
        magic_value += 5;
      }
      if(i == 3) {
        magic_value += 7;
      }
      if(i == 4) {
        magic_value += 11;
      }
      if(i == 5) {
        magic_value += 13;
      }
      if(i == 6) {
        magic_value += 17;
      }
      if(i == 7) {
        magic_value += 19;
      }
    }
  }

  printf("magic %d\n", magic_value);

  if(success_count == chksum_count) {
    // Cause an 'invalid read' crash
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

  if (argc < 4) {
    printf("usage: checksum <chksum_count> <chksum_len> <file_in>\n");
    exit(-2);
  }

  int chksum_count = atoi(argv[1]);
  int chksum_length = atoi(argv[2]);

  if ((fd = open(argv[3], O_RDONLY)) < 0) {
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

  vulnerable(buffer, chksum_count, chksum_length);

  return 0;
}
