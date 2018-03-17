/*
 * Inspired by example code from Guillaume Cottenceau.
 * http://zarb.org/~gc/html/libpng.html
 */

#include <png.h>
#include <stdlib.h> // malloc

int x, y;

int width, height;
png_byte color_type;
png_byte bit_depth;

png_structp png_ptr;
png_infop info_ptr;
int number_of_passes;
png_bytep * row_pointers;


int read_png_file(char* file_name)
{
  char header[8];    // 8 is the maximum size that can be checked

  /* open file and test for it being a png */
  FILE *fp = fopen(file_name, "rb");
  if (!fp)
    return -1;
  fread(header, 1, 8, fp);
  if (png_sig_cmp(header, 0, 8))
    return -1;

  /* initialize stuff */
  png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);

  if (!png_ptr)
    return -1;

  info_ptr = png_create_info_struct(png_ptr);
  if (!info_ptr)
    return -1;

  if (setjmp(png_jmpbuf(png_ptr)))
    return -1;

  png_init_io(png_ptr, fp);
  png_set_sig_bytes(png_ptr, 8);

  png_read_info(png_ptr, info_ptr);

  width = png_get_image_width(png_ptr, info_ptr);
  height = png_get_image_height(png_ptr, info_ptr);
  color_type = png_get_color_type(png_ptr, info_ptr);
  bit_depth = png_get_bit_depth(png_ptr, info_ptr);

  number_of_passes = png_set_interlace_handling(png_ptr);
  png_read_update_info(png_ptr, info_ptr);


  /* read file */
  if (setjmp(png_jmpbuf(png_ptr)))
    return -1;

  row_pointers = (png_bytep*) malloc(sizeof(png_bytep) * height);
  for (y=0; y<height; y++)
    row_pointers[y] = (png_byte*) malloc(png_get_rowbytes(png_ptr,info_ptr));

  png_read_image(png_ptr, row_pointers);

  fclose(fp);
  return (0);
}

int process_file(void)
{
  if (png_get_color_type(png_ptr, info_ptr) == PNG_COLOR_TYPE_RGB)
    return -1;

  // if (png_get_color_type(png_ptr, info_ptr) != PNG_COLOR_TYPE_RGBA)
  //   return -1;

  return 0;
}

int main(int argc, char **argv)
{
  if (argc != 2) {
    printf("Usage: program_name <file_in>\n");
    return -2;
  }
  else if (read_png_file(argv[1]) != -1) {
    return process_file();
  }

  return -1;
}
