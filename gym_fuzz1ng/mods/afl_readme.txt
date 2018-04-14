## Afl documentation
Ref: version 2.52b

During compilation, theses steps are performed by afl-as.c with (219) static void add_instrumentation(void)

This proc is called on pre-asm code to add instrumentation blocks. It checks for .code32 or .code64 blocks. Two types of code are added: 
	- Type 1: trampolines (many added)
	- Type 2: main payload (only once)


Main payload is added with: (447) fputs(use_64bit ? main_payload_64 : main_payload_32, outf);

*trampoline*:

(368)    fprintf(outf, use_64bit ? trampoline_fmt_64 : trampoline_fmt_32, R(MAP_SIZE));

R(MAP_SIZE) => random byte beteen 0 and MAP_SIZE, this is the cur_location = <COMPILE_TIME_RANDOM>; mentionned in http://lcamtuf.coredump.cx/afl/technical_details.txt.


The trampoline is added at this condition, just after the instruction (NOT taken branch), and at the beginning of destination (TAKEN branch)
	(366)	if (line[1] == 'j' && line[2] != 'm' && R(100) < inst_ratio) {
meaning that trampoline is added in theses cases:

	jmp					NO
	call 				NO
	jz/jnz				YES
	jc/jnc				YES
	jl/jg/jle/jge		YES

With an extra feature named instrumentation ratio, that is a probability to instrument (default = 100, set by a gloval ENV variable).

Trampolines and main payload are found in afl-as.h file.

A trampoline does the following:
	- saves registers edi/ecx/edx/eax (32 bits) or rdx,rcx,rax (64-bits) on the stack
	- call __afl_maybe_log with a parameter in ecx/rcx corresponding to R(MAP_SIZE) (see above, fprintf line 368 of .c file)
	
__afl_maybe_log is inside main_payload and does the following:
	- if SHM is not mapped, map it, connect with forkserver, etc.
	- __afl_store does the essential storage like this:

				#ifndef COVERAGE_ONLY
				  "  movl __afl_prev_loc, %edi\n"
				  "  xorl %ecx, %edi\n"
				  "  shrl $1, %ecx\n"
				  "  movl %ecx, __afl_prev_loc\n"
				#else
				  "  movl %ecx, %edi\n"
				#endif /* ^!COVERAGE_ONLY */
				  "\n"
				#ifdef SKIP_COUNTS
				  "  orb  $1, (%edx, %edi, 1)\n"
				#else
				  "  incb (%edx, %edi, 1)\n"
				#endif /* ^SKIP_COUNTS */


Meaning exactly:
			  	cur_location = <COMPILE_TIME_RANDOM>;			=> ecx
	  			shared_mem[cur_location ^ prev_location]++; 	=> prev_location is edi
	  			prev_location = cur_location >> 1;

Possible variant (if you #define SKIP_COUNTS):
				shared_mem[cur_location ^ prev_location] = 1; instead of a "++" that can overflow.


And that's it.

