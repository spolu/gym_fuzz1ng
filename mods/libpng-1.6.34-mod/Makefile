# libpng target Makefile
#
# Builds libpng using our moded afl version.

LIBPNGDIR=libpng-1.6.34
LIBAPATH=/.libs/libpng16.a

# we need zlib + libmath (pow)
ADDITIONS=-lz -lm
ADDITIONS_NOLM=-lz

all: $(LIBPNGDIRAFL)/$(LIBAPATH) $(LIBPNGDIR)/$(LIBAPATH) libpng_simple_fopen libpng_simple_fopen_afl libpng_simple_memory libpng_simple_unicorn libpng_simple_fopen_static

clean:
	rm -rf *.o
	rm -rf *.bin
	rm -rf libpng_simple_fopen
	rm -rf libpng_simple_fopen_afl
	rm -rf libpng_simple_fopen_static
	rm -rf libpng_simple_memory
	rm -rf libpng_simple_unicorn
	rm -rf *.offset
	cd $(LIBPNGDIR)/ && make clean
	cd $(LIBPNGDIRAFL)/ && make clean

$(LIBPNGDIRAFL)/$(LIBAPATH): 
	@echo " ****"
	@echo " **** Building libpng with afl instrumentation"
	@echo " ****"
	cd $(LIBPNGDIRAFL) && ./configure -q CC="afl-gcc" CXX="afl-g++" --enable-static --disable-shared; make

$(LIBPNGDIR)/$(LIBAPATH): 
	@echo " ****"
	@echo " **** Building libpng"
	@echo " ****"
	cd $(LIBPNGDIR) && ./configure -q --disable-shared --enable-static; make

#
# compile as a stand-alone testing binary (use system installed libpng)
# loads PNG from disk using libpng API
#
libpng_simple_fopen: libpng_simple_fopen.o
	@echo " ****"
	@echo " **** Building libpng_simple_fopen"
	@echo " ****"
	$(CC) libpng_simple_fopen.c -o libpng_simple_fopen -lpng $(ADDITIONS)

#
# compile for afl (static lib compiled for afl)
#
libpng_simple_fopen_afl: libpng_simple_fopen.o $(LIBPNGDIRAFL)/$(LIBAPATH)
	@echo " ****"
	@echo " **** Building libpng_simple_fopen_afl"
	@echo " ****"
	$(AFLCC) libpng_simple_fopen.c $(LIBPNGDIRAFL)/$(LIBAPATH) -o libpng_simple_fopen_afl $(ADDITIONS) -I $(LIBPNGDIRAFL)

#
# compile for pin (static lib)
#
libpng_simple_fopen_static: libpng_simple_fopen.o $(LIBPNGDIR)/$(LIBAPATH)
	@echo " ****"
	@echo " **** Building libpng_simple_fopen_static"
	@echo " ****"
	$(CC) libpng_simple_fopen.c $(LIBPNGDIR)/$(LIBAPATH) -o libpng_simple_fopen_static $(ADDITIONS) -I $(LIBPNGDIR)

#
# compile as a stand-alone testing binary (use system installed libpng)
# Manually loads PNG from disk, then reads PNG in memory (no disk IO libpng API)
#
libpng_simple_memory: libpng_simple_memory.o
	@echo " ****"
	@echo " **** Building libpng_simple_memory"
	@echo " ****"
	$(CC) libpng_simple_memory.c -o libpng_simple_memory -lpng $(ADDITIONS)

#
# compile a .bin for use with unicorn
# Manually loads PNG from fixed mem addr, then reads PNG in memory (no disk IO libpng API)
#
# .text code address is: 0x01000000 and must be equal to UNICORN CODE_ADDRESS define
#
# This will display addresses of <main> and of <stopaddr>
#
#
libpng_simple_unicorn: libpng_simple_unicorn.o
	@echo " ****"
	@echo " **** Building libpng_simple_unicorn"
	@echo " ****"
	# 
	$(CC) -std=gnu99 -Wimplicit-function-declaration -fno-stack-protector -Wl,--section-start=.text=0x01000000 \
		 -fPIC -fno-builtin -nostdlib stubstart.S  libpng_simple_unicorn.c $(LIBPNGDIR)/$(LIBAPATH) \
		 -T linker.lds -static -o libpng_simple_unicorn $(ADDITIONS_NOLM) -I $(LIBPNGDIR)/
	#$(CC) -std=gnu99 -Wimplicit-function-declaration -fno-stack-protector -Wl,--section-start=.text=0x01000000 libpng_simple_unicorn.c $(LIBPNGDIR)/.libs/libpng16.a -static -o libpng_simple_unicorn $(ADDITIONS) -I $(LIBPNGDIR)/
	objcopy -j .text -O binary libpng_simple_unicorn libpng_simple_unicorn.bin
	objdump -d libpng_simple_unicorn | awk -v RS= '/^[[:xdigit:]].*<_start>/'
	objdump -d libpng_simple_unicorn | grep ">:" > libpng_simple_unicorn.offsets

# sanity checks
test: all
	@echo " ****"
	@echo " **** testing everything"
	@echo " ****"
	./maketests.sh
