#include <stdio.h> // printf

int main(int argc, char **argv)
{
  if (argc != 2) {
    printf("Usage: simple_bits <file_in>\n");
    return -2;
  }

  FILE *fp = fopen(argv[1], "rb");
  if (!fp)
    return -1;

  return 0;
}
