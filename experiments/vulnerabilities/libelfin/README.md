# SEGV in function line_table::line_table at dwarf/line.cc:104

Tested in Ubuntu 16.04, 64bit.

The tested program is the example program dump-lines.

The testcase is [dump_line_segv](dump_line_segv).

I use the following command:

```
/path-to-libelfin/examples/dump-lines dump_line_segv
```
and got:

```
Segmentation fault (core dumped)
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
valgrind /path-to-libelfin/examples/dump-lines dump_line_segv
==4796== Memcheck, a memory error detector
==4796== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==4796== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==4796== Command: /path-to-libelfin/examples/dump-lines dump_line_segv
==4796== 
==4796== Invalid write of size 1
==4796==    at 0x47DA88: dwarf::line_table::line_table(std::shared_ptr<dwarf::section> const&, unsigned long, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) (line.cc:104)
==4796==    by 0x413558: dwarf::compilation_unit::get_line_table() const (dwarf.cc:304)
==4796==    by 0x402CB7: main (dump-lines.cc:41)
==4796==  Address 0x0 is not stack'd, malloc'd or (recently) free'd
==4796== 
==4796== 
==4796== Process terminating with default action of signal 11 (SIGSEGV)
==4796==  Access not within mapped region at address 0x0
==4796==    at 0x47DA88: dwarf::line_table::line_table(std::shared_ptr<dwarf::section> const&, unsigned long, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) (line.cc:104)
==4796==    by 0x413558: dwarf::compilation_unit::get_line_table() const (dwarf.cc:304)
==4796==    by 0x402CB7: main (dump-lines.cc:41)
==4796==  If you believe this happened as a result of a stack
==4796==  overflow in your program's main thread (unlikely but
==4796==  possible), you can try to increase the size of the
==4796==  main thread stack using the --main-stacksize= flag.
==4796==  The main thread stack size used in this run was 8388608.
--- <0>
==4796== 
==4796== HEAP SUMMARY:
==4796==     in use at exit: 81,475 bytes in 72 blocks
==4796==   total heap usage: 132 allocs, 60 frees, 89,399 bytes allocated
==4796== 
==4796== LEAK SUMMARY:
==4796==    definitely lost: 0 bytes in 0 blocks
==4796==    indirectly lost: 0 bytes in 0 blocks
==4796==      possibly lost: 0 bytes in 0 blocks
==4796==    still reachable: 81,475 bytes in 72 blocks
==4796==         suppressed: 0 bytes in 0 blocks
==4796== Rerun with --leak-check=full to see details of leaked memory
==4796== 
==4796== For counts of detected and suppressed errors, rerun with: -v
==4796== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)

```
I use **AddressSanitizer** to build ffjpeg and running it with the following command:

```
/path-to-libelfin/examples/dump-lines dump_line_segv
```

This is the ASAN information (absolute path information omitted):

```
/path-to-libelfin-address/examples/dump-lines dump_line_segv
ASAN:SIGSEGV
=================================================================
==4850==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 (pc 0x00000043b335 bp 0x7fff42876e40 sp 0x7fff428769e0 T0)
    #0 0x43b334 in dwarf::line_table::line_table(std::shared_ptr<dwarf::section> const&, unsigned long, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /path-to-libelfin-address/dwarf/line.cc:104
    #1 0x40f67b in dwarf::compilation_unit::get_line_table() const /path-to-libelfin-address/dwarf/dwarf.cc:304
    #2 0x403356 in main /path-to-libelfin-address/examples/dump-lines.cc:41
    #3 0x7f82f990682f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #4 0x403888 in _start (/path-to-libelfin-address/examples/dump-lines+0x403888)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /path-to-libelfin-address/dwarf/line.cc:104 dwarf::line_table::line_table(std::shared_ptr<dwarf::section> const&, unsigned long, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)
==4850==ABORTING
```

An attacker can exploit this vulnerability by submitting a malicious elf file that exploits this bug which will result in a Denial of Service (DoS).

# SEGV in function dwarf::cursor::skip_form at dwarf/cursor.cc:181

Tested in Ubuntu 16.04, 64bit.

The tested program is the example program dump-lines.

The testcase is [dump_line_segv2](dump_line_segv2).

I use the following command:

```
/path-to-libelfin/examples/dump-lines dump_line_segv2
```
and got:

```
Segmentation fault (core dumped)
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
valgrind /path-to-libelfin/examples/dump-lines dump_line_segv2
==11807== Memcheck, a memory error detector
==11807== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==11807== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==11807== Command: /path-to-libelfin/examples/dump-lines dump_line_segv2
==11807== 
==11807== Invalid read of size 1
==11807==    at 0x42A39C: dwarf::cursor::skip_form(dwarf::DW_FORM) (cursor.cc:181)
==11807==    by 0x431FAC: dwarf::die::read(unsigned long) (die.cc:51)
==11807==    by 0x412EFC: dwarf::unit::root() const (dwarf.cc:195)
==11807==    by 0x413177: dwarf::compilation_unit::get_line_table() const (dwarf.cc:291)
==11807==    by 0x402CB7: main (dump-lines.cc:41)
==11807==  Address 0x10cd80af is not stack'd, malloc'd or (recently) free'd
==11807== 
==11807== 
==11807== Process terminating with default action of signal 11 (SIGSEGV)
==11807==  Access not within mapped region at address 0x10CD80AF
==11807==    at 0x42A39C: dwarf::cursor::skip_form(dwarf::DW_FORM) (cursor.cc:181)
==11807==    by 0x431FAC: dwarf::die::read(unsigned long) (die.cc:51)
==11807==    by 0x412EFC: dwarf::unit::root() const (dwarf.cc:195)
==11807==    by 0x413177: dwarf::compilation_unit::get_line_table() const (dwarf.cc:291)
==11807==    by 0x402CB7: main (dump-lines.cc:41)
==11807==  If you believe this happened as a result of a stack
==11807==  overflow in your program's main thread (unlikely but
==11807==  possible), you can try to increase the size of the
==11807==  main thread stack using the --main-stacksize= flag.
==11807==  The main thread stack size used in this run was 8388608.
--- <0>
==11807== 
==11807== HEAP SUMMARY:
==11807==     in use at exit: 80,832 bytes in 64 blocks
==11807==   total heap usage: 122 allocs, 58 frees, 88,640 bytes allocated
==11807== 
==11807== LEAK SUMMARY:
==11807==    definitely lost: 0 bytes in 0 blocks
==11807==    indirectly lost: 0 bytes in 0 blocks
==11807==      possibly lost: 0 bytes in 0 blocks
==11807==    still reachable: 80,832 bytes in 64 blocks
==11807==         suppressed: 0 bytes in 0 blocks
==11807== Rerun with --leak-check=full to see details of leaked memory
==11807== 
==11807== For counts of detected and suppressed errors, rerun with: -v
==11807== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)

```
I use **AddressSanitizer** to build ffjpeg and running it with the following command:

```
/path-to-libelfin/examples/dump-lines dump_line_segv2
```

This is the ASAN information (absolute path information omitted):

```
/path-to-libelfin-address/examples/dump-lines dump_line_segv2
ASAN:SIGSEGV
=================================================================
==11879==ERROR: AddressSanitizer: SEGV on unknown address 0x7fc5c7ec50af (pc 0x000000416720 bp 0x7fffc67fa700 sp 0x7fffc67fa600 T0)
    #0 0x41671f in dwarf::cursor::skip_form(dwarf::DW_FORM) /path-to-libelfin-address/dwarf/cursor.cc:181
    #1 0x418023 in dwarf::die::read(unsigned long) /path-to-libelfin-address/dwarf/die.cc:51
    #2 0x40f158 in dwarf::unit::root() const /path-to-libelfin-address/dwarf/dwarf.cc:195
    #3 0x40f41e in dwarf::compilation_unit::get_line_table() const /path-to-libelfin-address/dwarf/dwarf.cc:291
    #4 0x403356 in main /path-to-libelfin-address/examples/dump-lines.cc:41
    #5 0x7fc5b96f682f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #6 0x403888 in _start (/path-to-libelfin-address/examples/dump-lines+0x403888)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /path-to-libelfin-address/dwarf/cursor.cc:181 dwarf::cursor::skip_form(dwarf::DW_FORM)
==11879==ABORTING
```

An attacker can exploit this vulnerability by submitting a malicious elf file that exploits this bug which will result in a Denial of Service (DoS).

# Global-Buffer-Overflow in function dwarf::line_table::line_table at dwarf/line.cc:107

Tested in Ubuntu 16.04, 64bit.

The tested program is the example program dump-lines.

The testcase is [dump_line_global_buffer_overflow](dump_line_global_buffer_overflow).

I use the following command:

```
/path-to-libelfin/examples/dump-lines dump_line_global_buffer_overflow
```

and get:

```
terminate called after throwing an instance of 'dwarf::format_error'
  what():  expected 858944595 arguments for line number opcode 16, got 2
--- <0>
Aborted (core dumped)
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
valgrind /path-to-libelfin/examples/dump-lines dump_line_global_buffer_overflow
==9235== Memcheck, a memory error detector
==9235== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==9235== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==9235== Command: /path-to-libelfin/examples/dump-lines dump_line_global_buffer_overflow
==9235== 
terminate called after throwing an instance of 'dwarf::format_error'
  what():  expected 858944595 arguments for line number opcode 16, got 2
--- <0>
==9235== 
==9235== Process terminating with default action of signal 6 (SIGABRT)
==9235==    at 0x546A428: raise (raise.c:54)
==9235==    by 0x546C029: abort (abort.c:89)
==9235==    by 0x4ED3DDD: ??? (in /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28)
==9235==    by 0x4EDF895: ??? (in /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28)
==9235==    by 0x4EDF900: std::terminate() (in /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28)
==9235==    by 0x4EDFB54: __cxa_throw (in /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.28)
==9235==    by 0x48226F: dwarf::line_table::line_table(std::shared_ptr<dwarf::section> const&, unsigned long, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) (line.cc:116)
==9235==    by 0x413558: dwarf::compilation_unit::get_line_table() const (dwarf.cc:304)
==9235==    by 0x402CB7: main (dump-lines.cc:41)
==9235== 
==9235== HEAP SUMMARY:
==9235==     in use at exit: 81,960 bytes in 75 blocks
==9235==   total heap usage: 139 allocs, 64 frees, 90,129 bytes allocated
==9235== 
==9235== LEAK SUMMARY:
==9235==    definitely lost: 0 bytes in 0 blocks
==9235==    indirectly lost: 0 bytes in 0 blocks
==9235==      possibly lost: 144 bytes in 1 blocks
==9235==    still reachable: 81,816 bytes in 74 blocks
==9235==                       of which reachable via heuristic:
==9235==                         stdstring          : 86 bytes in 1 blocks
==9235==         suppressed: 0 bytes in 0 blocks
==9235== Rerun with --leak-check=full to see details of leaked memory
==9235== 
==9235== For counts of detected and suppressed errors, rerun with: -v
==9235== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
Aborted (core dumped)
```

I use **AddressSanitizer** to build ffjpeg and running it with the following command:

```
/path-to-libelfin/examples/dump-lines dump_line_global_buffer_overflow
```

This is the ASAN information (absolute path information omitted):

```
/path-to-libelfin-address/examples/dump-lines dump_line_global_buffer_overflow
=================================================================
==9296==ERROR: AddressSanitizer: global-buffer-overflow on address 0x00000045f374 at pc 0x00000043db90 bp 0x7fff57889ea0 sp 0x7fff57889e90
READ of size 4 at 0x00000045f374 thread T0
    #0 0x43db8f in dwarf::line_table::line_table(std::shared_ptr<dwarf::section> const&, unsigned long, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /path-to-libelfin-address/dwarf/line.cc:107
    #1 0x40f67b in dwarf::compilation_unit::get_line_table() const /path-to-libelfin-address/dwarf/dwarf.cc:304
    #2 0x403356 in main /path-to-libelfin-address/examples/dump-lines.cc:41
    #3 0x7f0bb309682f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #4 0x403888 in _start (/path-to-libelfin-address/examples/dump-lines+0x403888)

0x00000045f374 is located 0 bytes to the right of global variable 'opcode_lengths' defined in 'line.cc:15:18' (0x45f340) of size 52
SUMMARY: AddressSanitizer: global-buffer-overflow /path-to-libelfin-address/dwarf/line.cc:107 dwarf::line_table::line_table(std::shared_ptr<dwarf::section> const&, unsigned long, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)
Shadow bytes around the buggy address:
  0x000080083e10: f9 f9 f9 f9 00 00 00 00 03 f9 f9 f9 f9 f9 f9 f9
  0x000080083e20: 00 00 00 00 00 00 00 00 04 f9 f9 f9 f9 f9 f9 f9
  0x000080083e30: 00 00 00 00 00 04 f9 f9 f9 f9 f9 f9 00 02 f9 f9
  0x000080083e40: f9 f9 f9 f9 00 00 00 00 03 f9 f9 f9 f9 f9 f9 f9
  0x000080083e50: 07 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
=>0x000080083e60: 04 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00[04]f9
  0x000080083e70: f9 f9 f9 f9 00 00 00 00 00 00 00 00 00 00 00 00
  0x000080083e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x000080083e90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x000080083ea0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x000080083eb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
==9296==ABORTING
```

An attacker can exploit this vulnerability by submitting a malicious elf file that exploits this bug which will result in a Denial of Service (DoS) even buffer overflow.

# SEGV in function elf::section::as_strtab at elf/elf.cc:284

Tested in Ubuntu 16.04, 64bit.

The tested program is the example program dump-syms.

The testcase is [dump_syms_segv](dump_syms_segv).

I use the following command:

```
/path-to-libelfin/examples/dump-syms dump_syms_segv
```

and get:

```
Segmentation fault (core dumped)
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
valgrind /path-to-libelfin/examples/dump-syms dump_syms_segv
==13575== Memcheck, a memory error detector
==13575== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==13575== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==13575== Command: /path-to-libelfin/examples/dump-syms dump_syms_segv
==13575== 
==13575== Invalid read of size 4
==13575==    at 0x40A8A3: elf::section::as_strtab() const (elf.cc:284)
==13575==    by 0x40BD91: elf::section::as_symtab() const (elf.cc:295)
==13575==    by 0x401FD8: main (dump-syms.cc:32)
==13575==  Address 0x14 is not stack'd, malloc'd or (recently) free'd
==13575== 
==13575== 
==13575== Process terminating with default action of signal 11 (SIGSEGV)
==13575==  Access not within mapped region at address 0x14
==13575==    at 0x40A8A3: elf::section::as_strtab() const (elf.cc:284)
==13575==    by 0x40BD91: elf::section::as_symtab() const (elf.cc:295)
==13575==    by 0x401FD8: main (dump-syms.cc:32)
==13575==  If you believe this happened as a result of a stack
==13575==  overflow in your program's main thread (unlikely but
==13575==  possible), you can try to increase the size of the
==13575==  main thread stack using the --main-stacksize= flag.
==13575==  The main thread stack size used in this run was 8388608.
Symbol table '.dynsym':
   Num: Value            Size  Type    Binding Index Name
==13575== 
==13575== HEAP SUMMARY:
==13575==     in use at exit: 79,384 bytes in 50 blocks
==13575==   total heap usage: 62 allocs, 12 frees, 84,776 bytes allocated
==13575== 
==13575== LEAK SUMMARY:
==13575==    definitely lost: 0 bytes in 0 blocks
==13575==    indirectly lost: 0 bytes in 0 blocks
==13575==      possibly lost: 0 bytes in 0 blocks
==13575==    still reachable: 79,384 bytes in 50 blocks
==13575==         suppressed: 0 bytes in 0 blocks
==13575== Rerun with --leak-check=full to see details of leaked memory
==13575== 
==13575== For counts of detected and suppressed errors, rerun with: -v
==13575== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)
```

I use **AddressSanitizer** to build ffjpeg and running it with the following command:

```
/path-to-libelfin/examples/dump-syms dump_syms_segv
```

This is the ASAN information (absolute path information omitted):

```
/path-to-libelfin-address/examples/dump-syms dump_syms_segv
ASAN:SIGSEGV
=================================================================
==13619==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000014 (pc 0x000000409050 bp 0x7ffdc34bbe50 sp 0x7ffdc34bbe10 T0)
    #0 0x40904f in elf::section::as_strtab() const /path-to-libelfin-address/elf/elf.cc:284
    #1 0x4099f5 in elf::section::as_symtab() const /path-to-libelfin-address/elf/elf.cc:295
    #2 0x4023fa in main /path-to-libelfin-address/examples/dump-syms.cc:32
    #3 0x7fae884aa82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #4 0x403728 in _start (/path-to-libelfin-address/examples/dump-syms+0x403728)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /path-to-libelfin-address/elf/elf.cc:284 elf::section::as_strtab() const
==13619==ABORTING
```

An attacker can exploit this vulnerability by submitting a malicious elf file that exploits this bug which will result in a Denial of Service (DoS) even buffer overflow.

# SEGV in function dwarf::cursor::uleb128 at dwarf/internal.hh:154

Tested in Ubuntu 16.04, 64bit.

The tested program is the example program dump-tree.

The testcase is [dump_tree_segv](dump_tree_segv).

I use the following command:

```
/path-to-libelfin/examples/dump-tree dump_tree_segv
```

and get:

```
Segmentation fault (core dumped)
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
valgrind /path-to-libelfin/examples/dump-tree dump_tree_segv
==21176== Memcheck, a memory error detector
==21176== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==21176== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==21176== Command: /path-to-libelfin/examples/dump-tree dump_tree_segv
==21176== 
==21176== Invalid read of size 1
==21176==    at 0x431161: uleb128 (internal.hh:154)
==21176==    by 0x431161: dwarf::die::read(unsigned long) (die.cc:35)
==21176==    by 0x44869E: dwarf::value::as_reference() const (value.cc:215)
==21176==    by 0x44C482: dwarf::to_string[abi:cxx11](dwarf::value const&) (value.cc:324)
==21176==    by 0x404A3B: dump_tree(dwarf::die const&, int) (dump-tree.cc:19)
==21176==    by 0x4035C1: dump_tree (dump-tree.cc:21)
==21176==    by 0x4035C1: main (dump-tree.cc:43)
==21176==  Address 0x5b02809b is not stack'd, malloc'd or (recently) free'd
==21176== 
==21176== 
==21176== Process terminating with default action of signal 11 (SIGSEGV)
==21176==  Access not within mapped region at address 0x5B02809B
==21176==    at 0x431161: uleb128 (internal.hh:154)
==21176==    by 0x431161: dwarf::die::read(unsigned long) (die.cc:35)
==21176==    by 0x44869E: dwarf::value::as_reference() const (value.cc:215)
==21176==    by 0x44C482: dwarf::to_string[abi:cxx11](dwarf::value const&) (value.cc:324)
==21176==    by 0x404A3B: dump_tree(dwarf::die const&, int) (dump-tree.cc:19)
==21176==    by 0x4035C1: dump_tree (dump-tree.cc:21)
==21176==    by 0x4035C1: main (dump-tree.cc:43)
==21176==  If you believe this happened as a result of a stack
==21176==  overflow in your program's main thread (unlikely but
==21176==  possible), you can try to increase the size of the
==21176==  main thread stack using the --main-stacksize= flag.
==21176==  The main thread stack size used in this run was 8388608.
--- <0>
<b> DW_TAG_compile_unit
      DW_AT_producer 
      DW_AT_language 4 byte block: cb 0 0 0
      DW_AT_name 
      DW_AT_comp_dir 
      DW_AT_low_pc 0x0
      DW_AT_high_pc 0x1500000000000000
      DW_AT_stmt_list <line 0x0>
 <2d> DW_TAG_base_type
       DW_AT_byte_size 0x8
       DW_AT_encoding 0x7
       DW_AT_name long unsigned int
 <34> DW_TAG_base_type
       DW_AT_byte_size 0x1
       DW_AT_encoding 0x8
       DW_AT_name 
 <3b> DW_TAG_base_type
       DW_AT_byte_size 0x2
       DW_AT_encoding 0x7
       DW_AT_name 
 <42> DW_TAG_base_type
       DW_AT_byte_size 0x4
       DW_AT_encoding 0x7
       DW_AT_name 
 <49> DW_TAG_base_type
       DW_AT_byte_size 0x1
       DW_AT_encoding 0x6
       DW_AT_name 
 <50> DW_TAG_base_type
       DW_AT_byte_size 0x2
       DW_AT_encoding 0x5
       DW_AT_name 
 <57> DW_TAG_base_type
       DW_AT_byte_size 0x4
       DW_AT_encoding 0x5
       DW_AT_name int
 <5e> DW_TAG_base_type
       DW_AT_byte_size 0x8
       DW_AT_encoding 0x5
       DW_AT_name 
 <65> DW_TAG_base_type
       DW_AT_byte_size 0x8
       DW_AT_encoding 0x7
       DW_AT_name 
 <6c> DW_TAG_base_type
       DW_AT_byte_size 0x1
       DW_AT_encoding 0x6
       DW_AT_name 
 <73> DW_TAG_subprogram
       DW_AT_external true
       DW_AT_name 
       DW_AT_decl_file 0x1
       DW_AT_decl_line 0x3
==21176== 
==21176== HEAP SUMMARY:
==21176==     in use at exit: 81,552 bytes in 68 blocks
==21176==   total heap usage: 182 allocs, 114 frees, 92,963 bytes allocated
==21176== 
==21176== LEAK SUMMARY:
==21176==    definitely lost: 0 bytes in 0 blocks
==21176==    indirectly lost: 0 bytes in 0 blocks
==21176==      possibly lost: 0 bytes in 0 blocks
==21176==    still reachable: 81,552 bytes in 68 blocks
==21176==         suppressed: 0 bytes in 0 blocks
==21176== Rerun with --leak-check=full to see details of leaked memory
==21176== 
==21176== For counts of detected and suppressed errors, rerun with: -v
==21176== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)
```

I use **AddressSanitizer** to build ffjpeg and running it with the following command:

```
/path-to-libelfin/examples/dump-tree dump_tree_segv
```

This is the ASAN information (absolute path information omitted):

```
/path-to-libelfin-address/examples/dump-tree dump_tree_segv
ASAN:SIGSEGV
=================================================================
==21215==ERROR: AddressSanitizer: SEGV on unknown address 0x7f519be3409b (pc 0x000000417cb5 bp 0x7ffddf8f6830 sp 0x7ffddf8f6730 T0)
    #0 0x417cb4 in dwarf::cursor::uleb128() /path-to-libelfin-address/dwarf/internal.hh:154
    #1 0x417cb4 in dwarf::die::read(unsigned long) /path-to-libelfin-address/dwarf/die.cc:35
    #2 0x422a25 in dwarf::value::as_reference() const /path-to-libelfin-address/dwarf/value.cc:215
    #3 0x425711 in dwarf::to_string[abi:cxx11](dwarf::value const&) /path-to-libelfin-address/dwarf/value.cc:324
    #4 0x403aec in dump_tree(dwarf::die const&, int) /path-to-libelfin-address/examples/dump-tree.cc:19
    #5 0x403bea in dump_tree(dwarf::die const&, int) /path-to-libelfin-address/examples/dump-tree.cc:21
    #6 0x403361 in main /path-to-libelfin-address/examples/dump-tree.cc:43
    #7 0x7f514331582f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #8 0x403878 in _start (/path-to-libelfin-address/examples/dump-tree+0x403878)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /path-to-libelfin-address/dwarf/internal.hh:154 dwarf::cursor::uleb128()
==21215==ABORTING
```

An attacker can exploit this vulnerability by submitting a malicious elf file that exploits this bug which will result in a Denial of Service (DoS).

# SEGV in function dwarf::to_string at dwarf/value.cc:300

Tested in Ubuntu 16.04, 64bit.

The tested program is the example program dump-tree.

The testcase is [dump_tree_segv2](dump_tree_segv2).

I use the following command:

```
/path-to-libelfin/examples/dump-tree dump_tree_segv2
```

and get:

```
Segmentation fault (core dumped)
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
valgrind /path-to-libelfin/examples/dump-tree dump_tree_segv2
==22094== Memcheck, a memory error detector
==22094== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==22094== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==22094== Command: /path-to-libelfin/examples/dump-tree dump_tree_segv2
==22094== 
==22094== Invalid read of size 1
==22094==    at 0x44CE58: dwarf::to_string[abi:cxx11](dwarf::value const&) (value.cc:300)
==22094==    by 0x4031B0: dump_tree (dump-tree.cc:19)
==22094==    by 0x4031B0: main (dump-tree.cc:43)
==22094==  Address 0x402a000 is not stack'd, malloc'd or (recently) free'd
==22094== 
==22094== 
==22094== Process terminating with default action of signal 11 (SIGSEGV)
==22094==  Access not within mapped region at address 0x402A000
==22094==    at 0x44CE58: dwarf::to_string[abi:cxx11](dwarf::value const&) (value.cc:300)
==22094==    by 0x4031B0: dump_tree (dump-tree.cc:19)
==22094==    by 0x4031B0: main (dump-tree.cc:43)
==22094==  If you believe this happened as a result of a stack
==22094==  overflow in your program's main thread (unlikely but
==22094==  possible), you can try to increase the size of the
==22094==  main thread stack using the --main-stacksize= flag.
==22094==  The main thread stack size used in this run was 8388608.
--- <0>
<b> DW_TAG_compile_unit
      DW_AT_producer 
      DW_AT_language 12 byte block: cb 0 0 0 12 0 0 0 26 5 40 0
      DW_AT_name long unsigned int
==22094== 
==22094== HEAP SUMMARY:
==22094==     in use at exit: 111,921 bytes in 68 blocks
==22094==   total heap usage: 145 allocs, 77 frees, 150,879 bytes allocated
==22094== 
==22094== LEAK SUMMARY:
==22094==    definitely lost: 0 bytes in 0 blocks
==22094==    indirectly lost: 0 bytes in 0 blocks
==22094==      possibly lost: 0 bytes in 0 blocks
==22094==    still reachable: 111,921 bytes in 68 blocks
==22094==         suppressed: 0 bytes in 0 blocks
==22094== Rerun with --leak-check=full to see details of leaked memory
==22094== 
==22094== For counts of detected and suppressed errors, rerun with: -v
==22094== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)
```

I use **AddressSanitizer** to build ffjpeg and running it with the following command:

```
/path-to-libelfin/examples/dump-tree dump_tree_segv2
Segmentation fault (core dumped)
```

This is the ASAN information (absolute path information omitted):

```
/path-to-libelfin-address/examples/dump-tree dump_tree_segv2
=================================================================
==22134==ERROR: AddressSanitizer: unknown-crash on address 0x7f6f8b233000 at pc 0x000000428213 bp 0x7ffd7ae677d0 sp 0x7ffd7ae677c0
READ of size 1 at 0x7f6f8b233000 thread T0
    #0 0x428212 in dwarf::to_string[abi:cxx11](dwarf::value const&) /path-to-libelfin-address/dwarf/value.cc:300
    #1 0x403aec in dump_tree(dwarf::die const&, int) /path-to-libelfin-address/examples/dump-tree.cc:19
    #2 0x403361 in main /path-to-libelfin-address/examples/dump-tree.cc:43
    #3 0x7f6f8971282f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #4 0x403878 in _start (/path-to-libelfin-address/examples/dump-tree+0x403878)

AddressSanitizer can not describe address in more detail (wild memory access suspected).
SUMMARY: AddressSanitizer: unknown-crash /path-to-libelfin-address/dwarf/value.cc:300 dwarf::to_string[abi:cxx11](dwarf::value const&)
Shadow bytes around the buggy address:
  0x0fee7163e5b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fee7163e5c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fee7163e5d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fee7163e5e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fee7163e5f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fee7163e600:[fe]fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe
  0x0fee7163e610: fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe
  0x0fee7163e620: fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe
  0x0fee7163e630: fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe
  0x0fee7163e640: fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe
  0x0fee7163e650: fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe fe
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
==22134==ABORTING
```

An attacker can exploit this vulnerability by submitting a malicious elf file that exploits this bug which will result in a Denial of Service (DoS).

# SEGV in function dwarf::cursor::skip_form at dwarf/cursor.cc:191

Tested in Ubuntu 16.04, 64bit.

The tested program is the example program dump-tree.

The testcase is [dump_tree_segv3](dump_tree_segv3).

I use the following command:

```
/path-to-libelfin/examples/dump-tree dump_tree_segv3
```

and get:

```
Segmentation fault (core dumped)
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
valgrind /path-to-libelfin/examples/dump-tree dump_tree_segv3
==423== Memcheck, a memory error detector
==423== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==423== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==423== Command: /path-to-libelfin/examples/dump-tree dump_tree_segv3
==423== 
==423== Invalid read of size 1
==423==    at 0x42C998: uleb128 (internal.hh:154)
==423==    by 0x42C998: dwarf::cursor::skip_form(dwarf::DW_FORM) (cursor.cc:147)
==423==    by 0x433B4C: dwarf::die::read(unsigned long) (die.cc:51)
==423==    by 0x414B7C: dwarf::unit::root() const (dwarf.cc:195)
==423==    by 0x402CD0: main (dump-tree.cc:43)
==423==  Address 0x750280b3 is not stack'd, malloc'd or (recently) free'd
==423== 
==423== 
==423== Process terminating with default action of signal 11 (SIGSEGV)
==423==  Access not within mapped region at address 0x750280B3
==423==    at 0x42C998: uleb128 (internal.hh:154)
==423==    by 0x42C998: dwarf::cursor::skip_form(dwarf::DW_FORM) (cursor.cc:147)
==423==    by 0x433B4C: dwarf::die::read(unsigned long) (die.cc:51)
==423==    by 0x414B7C: dwarf::unit::root() const (dwarf.cc:195)
==423==    by 0x402CD0: main (dump-tree.cc:43)
==423==  If you believe this happened as a result of a stack
==423==  overflow in your program's main thread (unlikely but
==423==  possible), you can try to increase the size of the
==423==  main thread stack using the --main-stacksize= flag.
==423==  The main thread stack size used in this run was 8388608.
--- <0>
==423== 
==423== HEAP SUMMARY:
==423==     in use at exit: 80,652 bytes in 63 blocks
==423==   total heap usage: 120 allocs, 57 frees, 88,208 bytes allocated
==423== 
==423== LEAK SUMMARY:
==423==    definitely lost: 0 bytes in 0 blocks
==423==    indirectly lost: 0 bytes in 0 blocks
==423==      possibly lost: 0 bytes in 0 blocks
==423==    still reachable: 80,652 bytes in 63 blocks
==423==         suppressed: 0 bytes in 0 blocks
==423== Rerun with --leak-check=full to see details of leaked memory
==423== 
==423== For counts of detected and suppressed errors, rerun with: -v
==423== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)
```

I use **AddressSanitizer** to build ffjpeg and running it with the following command:

```
/path-to-libelfin/examples/dump-tree dump_tree_segv3
```

This is the ASAN information (absolute path information omitted):

```
/path-to-libelfin-address/examples/dump-tree dump_tree_segv3
ASAN:SIGSEGV
=================================================================
==451==ERROR: AddressSanitizer: SEGV on unknown address 0x7f84237480b3 (pc 0x0000004167e8 bp 0x7fff99fc19f0 sp 0x7fff99fc18f0 T0)
    #0 0x4167e7 in dwarf::cursor::skip_form(dwarf::DW_FORM) /path-to-libelfin-address/dwarf/cursor.cc:191
    #1 0x4183b3 in dwarf::die::read(unsigned long) /path-to-libelfin-address/dwarf/die.cc:51
    #2 0x40f548 in dwarf::unit::root() const /path-to-libelfin-address/dwarf/dwarf.cc:195
    #3 0x403357 in main /path-to-libelfin-address/examples/dump-tree.cc:43
    #4 0x7f83b0c2982f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #5 0x403878 in _start (/path-to-libelfin-address/examples/dump-tree+0x403878)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV /path-to-libelfin-address/dwarf/cursor.cc:191 dwarf::cursor::skip_form(dwarf::DW_FORM)
==451==ABORTING
```

An attacker can exploit this vulnerability by submitting a malicious elf file that exploits this bug which will result in a Denial of Service (DoS).
