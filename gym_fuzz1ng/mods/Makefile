# Builds afl altered by our mod for external fuzzing as well as all of our
# targets.

# AFL

AFL_VERSION=2.52b
AFL_MOD=afl-$(AFL_VERSION)-mod
AFL_DIR=$(AFL_MOD)/afl-$(AFL_VERSION)

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

AFL_FUZZ=$(ROOT_DIR)/$(AFL_DIR)/afl-fuzz
AFL_GCC=$(ROOT_DIR)/$(AFL_DIR)/afl-gcc
AFL_GXX=$(ROOT_DIR)/$(AFL_DIR)/afl-g++

$(AFL_DIR):
	@echo " **** Downloading afl and applying fuzz1ng mod"
	cd $(AFL_MOD)/ && wget http://lcamtuf.coredump.cx/afl/releases/afl-$(AFL_VERSION).tgz
	cd $(AFL_MOD)/ && tar xvf afl-$(AFL_VERSION).tgz
	cp -R $(AFL_MOD)/mod/* $(AFL_DIR)/

$(AFL_DIR)/afl-fuzz: $(AFL_DIR)
	@echo " **** Building afl with fuzz1ng mod"
	cd $(AFL_DIR)/ && make

# LIBPNG

LIBPNG_VERSION=1.6.34

LIBPNG_MOD=libpng-$(LIBPNG_VERSION)-mod
LIBPNG_DIR=$(LIBPNG_MOD)/libpng-$(LIBPNG_VERSION)
LIBPNG_A_PATH=/.libs/libpng16.a

$(LIBPNG_DIR):
	@echo " **** Downloading libpng"
	cd $(LIBPNG_MOD) && \
	  wget https://freefr.dl.sourceforge.net/project/libpng/libpng16/1.6.34/libpng-$(LIBPNG_VERSION).tar.gz \
	  -O libpng-$(LIBPNG_VERSION).tar.gz
	cd $(LIBPNG_MOD) && tar xzf libpng-$(LIBPNG_VERSION).tar.gz

$(LIBPNG_DIR)/$(LIBPNG_A_PATH): $(LIBPNG_DIR)
	@echo " **** Building libpng with afl"
	cd $(LIBPNG_DIR) && ./configure -q CC="$(AFL_GCC)" CXX="$(AFL_GXX)" --enable-static --disable-shared; make

$(LIBPNG_MOD)/libpng_simple_fopen_afl: $(LIBPNG_DIR)/$(LIBPNG_A_PATH)
	@echo " **** Building libpng_simple_fopen_afl"
	cd $(LIBPNG_MOD) && $(AFL_GCC) libpng_simple_fopen.c \
	  libpng-$(LIBPNG_VERSION)/$(LIBPNG_A_PATH) \
	  -o libpng_simple_fopen_afl -lz -lm -I libpng-$(LIBPNG_VERSION)

# SIMPLE_BITS

SIMPLE_BITS_MOD=simple_bits-mod

$(SIMPLE_BITS_MOD)/simple_bits_afl:
	@echo " **** Building libpng_simple_bits_afl"
	cd $(SIMPLE_BITS_MOD) && $(AFL_GCC) simple_bits_afl.c \
	  -o simple_bits_afl -lz -lm


# ALL

all: $(AFL_DIR)/afl-fuzz \
  $(LIBPNG_DIR)/$(LIBPNG_A_PATH) $(LIBPNG_MOD)/libpng_simple_fopen_afl \
  $(SIMPLE_BITS_MOD)/simple_bits_afl

clean:
	rm -rf $(AFL_DIR)
	rm -rf $(AFL_MOD)/afl-$(AFL_VERSION).tgz
	rm -rf $(LIBPNG_DIR)
	rm -rf $(LIBPNG_MOD)/libpng-$(LIBPNG_VERSION).tar.gz
	rm -rf $(LIBPNG_MOD)/libpng_simple_fopen_afl
	rm -rf $(SIMPLE_BITS_MOD)/simple_bits_afl
