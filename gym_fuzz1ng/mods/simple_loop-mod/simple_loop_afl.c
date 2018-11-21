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

static int y = 0;

void noop(int i)
{
  y += time(NULL);
  printf("bar %d\n", i);
}

void vulnerable(unsigned char* data_buf)
{
  printf("fooo %d %d\n", data_buf[0], data_buf[1]);

  if(data_buf[0] == 42) {
    int x = 0;
    time_t y = 0;
    for(int i = 0; i < (int)data_buf[1]; i++) {
      // gimmicky to make sure we use a conditional jump.
      if (i < (int)data_buf[0]) {
        noop(i);
      }
      // Cause looping through transitions based on data[1].
      x += i;
    }

    printf("bar %d\n", y);

    if(x == 78) {
      // Cause an 'invalid read' crash if data[0..1] == "\x42\x13".
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
