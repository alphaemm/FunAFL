# heap-buffer-overflow in function process_DQT at jpgqguess.c:111

Tested in Ubuntu 16.04, 64bit.

The version of jhead is v3.04.

The testcase is [jhead_autorot_heap_buffer_overflow](jhead_autorot_heap_buffer_overflow).

I use the following command:

```
jhead -autorot jhead_autorot_heap_buffer_overflow
```

and get:

```
many Notfatal Error messages like below: 
Nonfatal Error : 'jhead_autorot_heap_buffer_overflow' Extraneous 36 padding bytes before section C0

Nonfatal Error : 'jhead_autorot_heap_buffer_overflow' Extraneous 11 padding bytes before section DB

......

Error : Premature end of file?
in file 'jhead_autorot_heap_buffer_overflow'
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
many Notfatal Error messages like below: 
Nonfatal Error : 'jhead_autorot_heap_buffer_overflow' Extraneous 36 padding bytes before section C0

Nonfatal Error : 'jhead_autorot_heap_buffer_overflow' Extraneous 11 padding bytes before section DB

......

==16221== Invalid read of size 1
==16221==    at 0x4193E9: process_DQT (jpgqguess.c:111)
==16221==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221==  Address 0x5558363 is 0 bytes after a block of size 6,211 alloc'd
==16221==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==16221==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221== 
==16221== Invalid read of size 1
==16221==    at 0x4193EF: process_DQT (jpgqguess.c:109)
==16221==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221==  Address 0x5558364 is 1 bytes after a block of size 6,211 alloc'd
==16221==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==16221==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221== 
==16221== Invalid read of size 1
==16221==    at 0x4193F9: process_DQT (jpgqguess.c:111)
==16221==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221==  Address 0x5558365 is 2 bytes after a block of size 6,211 alloc'd
==16221==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==16221==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221== 
==16221== Invalid read of size 1
==16221==    at 0x41941E: process_DQT (jpgqguess.c:109)
==16221==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221==  Address 0x5558366 is 3 bytes after a block of size 6,211 alloc'd
==16221==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==16221==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221== 
==16221== Invalid read of size 1
==16221==    at 0x419449: process_DQT (jpgqguess.c:111)
==16221==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221==  Address 0x5558367 is 4 bytes after a block of size 6,211 alloc'd
==16221==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==16221==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221== 
==16221== Invalid read of size 1
==16221==    at 0x4193D0: process_DQT (jpgqguess.c:109)
==16221==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221==  Address 0x5558368 is 5 bytes after a block of size 6,211 alloc'd
==16221==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==16221==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221== 
==16221== Invalid read of size 1
==16221==    at 0x4193D5: process_DQT (jpgqguess.c:111)
==16221==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221==  Address 0x5558369 is 6 bytes after a block of size 6,211 alloc'd
==16221==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==16221==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221== 
==16221== Invalid read of size 1
==16221==    at 0x4193E3: process_DQT (jpgqguess.c:109)
==16221==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221==  Address 0x555836a is 7 bytes after a block of size 6,211 alloc'd
==16221==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==16221==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==16221==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==16221==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==16221==    by 0x408484: ProcessFile (jhead.c:849)
==16221==    by 0x4022C3: main (jhead.c:1756)
==16221== 

Error : Premature end of file?
in file 'jhead_autorot_heap_buffer_overflow'
==16221== 
==16221== HEAP SUMMARY:
==16221==     in use at exit: 106,347 bytes in 1,813 blocks
==16221==   total heap usage: 1,831 allocs, 18 frees, 170,059 bytes allocated
==16221== 
==16221== LEAK SUMMARY:
==16221==    definitely lost: 0 bytes in 0 blocks
==16221==    indirectly lost: 0 bytes in 0 blocks
==16221==      possibly lost: 0 bytes in 0 blocks
==16221==    still reachable: 106,347 bytes in 1,813 blocks
==16221==         suppressed: 0 bytes in 0 blocks
==16221== Rerun with --leak-check=full to see details of leaked memory
==16221== 
==16221== For counts of detected and suppressed errors, rerun with: -v
==16221== ERROR SUMMARY: 61 errors from 8 contexts (suppressed: 0 from 0)
```

I use **AddressSanitizer** to build jhead and running it with the following command:

```
jhead -autorot jhead_autorot_heap_buffer_overflow
```

This is the ASAN information (absolute path information omitted):

```
many Notfatal Error messages like below: 
Nonfatal Error : 'jhead_autorot_heap_buffer_overflow' Extraneous 27 padding bytes before section ED

Nonfatal Error : 'jhead_autorot_heap_buffer_overflow' Extraneous 36 padding bytes before section C0

Nonfatal Error : 'jhead_autorot_heap_buffer_overflow' Extraneous 11 padding bytes before section DB
=================================================================
==19385==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x62300000f943 at pc 0x00000040a154 bp 0x7ffee7a5b910 sp 0x7ffee7a5b900
READ of size 1 at 0x62300000f943 thread T0
    #0 0x40a153 in process_DQT jpgqguess.c:111
    #1 0x407e02 in ReadJpegSections jpgfile.c:223
    #2 0x408581 in ReadJpegFile jpgfile.c:379
    #3 0x404e41 in ProcessFile jhead.c:849
    #4 0x40267d in main jhead.c:1756
    #5 0x7f1b3ce2f82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #6 0x403c38 in _start (jhead+0x403c38)

0x62300000f943 is located 0 bytes to the right of 6211-byte region [0x62300000e100,0x62300000f943)
allocated by thread T0 here:
    #0 0x7f1b3d57a662 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x98662)
    #1 0x40798b in ReadJpegSections jpgfile.c:173
    #2 0x408581 in ReadJpegFile jpgfile.c:379
    #3 0x404e41 in ProcessFile jhead.c:849
    #4 0x40267d in main jhead.c:1756
    #5 0x7f1b3ce2f82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-buffer-overflow jpgqguess.c:111 process_DQT
Shadow bytes around the buggy address:
  0x0c467fff9ed0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c467fff9ee0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c467fff9ef0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c467fff9f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c467fff9f10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c467fff9f20: 00 00 00 00 00 00 00 00[03]fa fa fa fa fa fa fa
  0x0c467fff9f30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c467fff9f40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c467fff9f50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c467fff9f60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c467fff9f70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==19385==ABORTING
```

# heap-buffer-overflow in function process_DQT at jpgqguess.c:109

Tested in Ubuntu 16.04, 64bit.

The version of jhead is v3.04.

The testcase is [jhead_mkexif_heap_buffer_overflow2](jhead_mkexif_heap_buffer_overflow2).

I use the following command:

```
jhead -mkexif jhead_mkexif_heap_buffer_overflow2
```

and get:

```
jhead -mkexif jhead_mkexif_heap_buffer_overflow2

Nonfatal Error : 'jhead_mkexif_heap_buffer_overflow2' DQT section too short

Nonfatal Error : 'jhead_mkexif_heap_buffer_overflow2' Extraneous 23 padding bytes before section DB

......

Error : Premature end of file?
in file 'jhead_mkexif_heap_buffer_overflow2'
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
many Notfatal Error messages like below: 
Nonfatal Error : 'jhead_mkexif_heap_buffer_overflow2' Extraneous 13 padding bytes before section DB

Nonfatal Error : 'jhead_mkexif_heap_buffer_overflow2' DQT section too short

......

==19299== Invalid read of size 1
==19299==    at 0x4193D0: process_DQT (jpgqguess.c:109)
==19299==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299==  Address 0x5551f11 is 0 bytes after a block of size 5,649 alloc'd
==19299==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==19299==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299== 
==19299== Invalid read of size 1
==19299==    at 0x4193D5: process_DQT (jpgqguess.c:111)
==19299==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299==  Address 0x5551f12 is 1 bytes after a block of size 5,649 alloc'd
==19299==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==19299==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299== 
==19299== Invalid read of size 1
==19299==    at 0x4193E3: process_DQT (jpgqguess.c:109)
==19299==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299==  Address 0x5551f13 is 2 bytes after a block of size 5,649 alloc'd
==19299==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==19299==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299== 
==19299== Invalid read of size 1
==19299==    at 0x4193E9: process_DQT (jpgqguess.c:111)
==19299==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299==  Address 0x5551f14 is 3 bytes after a block of size 5,649 alloc'd
==19299==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==19299==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299== 
==19299== Invalid read of size 1
==19299==    at 0x4193EF: process_DQT (jpgqguess.c:109)
==19299==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299==  Address 0x5551f15 is 4 bytes after a block of size 5,649 alloc'd
==19299==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==19299==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299== 
==19299== Invalid read of size 1
==19299==    at 0x4193F9: process_DQT (jpgqguess.c:111)
==19299==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299==  Address 0x5551f16 is 5 bytes after a block of size 5,649 alloc'd
==19299==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==19299==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299== 
==19299== Invalid read of size 1
==19299==    at 0x41941E: process_DQT (jpgqguess.c:109)
==19299==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299==  Address 0x5551f17 is 6 bytes after a block of size 5,649 alloc'd
==19299==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==19299==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299== 
==19299== Invalid read of size 1
==19299==    at 0x419449: process_DQT (jpgqguess.c:111)
==19299==    by 0x410BF5: ReadJpegSections.part.0 (jpgfile.c:223)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299==  Address 0x5551f18 is 7 bytes after a block of size 5,649 alloc'd
==19299==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==19299==    by 0x4102E6: ReadJpegSections.part.0 (jpgfile.c:173)
==19299==    by 0x41289E: ReadJpegSections (jpgfile.c:126)
==19299==    by 0x41289E: ReadJpegFile (jpgfile.c:379)
==19299==    by 0x408E8E: ProcessFile (jhead.c:905)
==19299==    by 0x4022C3: main (jhead.c:1756)
==19299== 

many Notfatal Error messages like below: 
Nonfatal Error : 'jhead_mkexif_heap_buffer_overflow2' DQT section too short

Nonfatal Error : 'jhead_mkexif_heap_buffer_overflow2' Extraneous 12 padding bytes before section DB

......

Error : Premature end of file?
in file 'jhead_mkexif_heap_buffer_overflow2'
==19299== 
==19299== HEAP SUMMARY:
==19299==     in use at exit: 108,798 bytes in 1,583 blocks
==19299==   total heap usage: 1,599 allocs, 16 frees, 172,126 bytes allocated
==19299== 
==19299== LEAK SUMMARY:
==19299==    definitely lost: 0 bytes in 0 blocks
==19299==    indirectly lost: 0 bytes in 0 blocks
==19299==      possibly lost: 0 bytes in 0 blocks
==19299==    still reachable: 108,798 bytes in 1,583 blocks
==19299==         suppressed: 0 bytes in 0 blocks
==19299== Rerun with --leak-check=full to see details of leaked memory
==19299== 
==19299== For counts of detected and suppressed errors, rerun with: -v
==19299== ERROR SUMMARY: 40 errors from 8 contexts (suppressed: 0 from 0)
```

I use **AddressSanitizer** to build jhead and running it with the following command:

```
jhead -mkexif jhead_mkexif_heap_buffer_overflow2
```

This is the ASAN information (absolute path information omitted):

```
many Notfatal Error messages like below: 
Nonfatal Error : 'jhead_mkexif_heap_buffer_overflow2' DQT section too short

Nonfatal Error : 'jhead_mkexif_heap_buffer_overflow2' Extraneous 26 padding bytes before section C4
=================================================================
==19316==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x62200001c711 at pc 0x00000040a14f bp 0x7fff9de6b520 sp 0x7fff9de6b510
READ of size 1 at 0x62200001c711 thread T0
    #0 0x40a14e in process_DQT jhead-3.04/jpgqguess.c:109
    #1 0x407e02 in ReadJpegSections jhead-3.04/jpgfile.c:223
    #2 0x408581 in ReadJpegFile jhead-3.04/jpgfile.c:379
    #3 0x405039 in ProcessFile jhead-3.04/jhead.c:905
    #4 0x40267d in main jhead-3.04/jhead.c:1756
    #5 0x7fbdfe0ea82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #6 0x403c38 in _start (install/jhead+0x403c38)

0x62200001c711 is located 0 bytes to the right of 5649-byte region [0x62200001b100,0x62200001c711)
allocated by thread T0 here:
    #0 0x7fbdfe835662 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x98662)
    #1 0x40798b in ReadJpegSections jhead-3.04/jpgfile.c:173
    #2 0x408581 in ReadJpegFile jhead-3.04/jpgfile.c:379
    #3 0x405039 in ProcessFile jhead-3.04/jhead.c:905
    #4 0x40267d in main jhead-3.04/jhead.c:1756
    #5 0x7fbdfe0ea82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-buffer-overflow jhead-3.04/jpgqguess.c:109 process_DQT
Shadow bytes around the buggy address:
  0x0c447fffb890: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c447fffb8a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c447fffb8b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c447fffb8c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c447fffb8d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c447fffb8e0: 00 00[01]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c447fffb8f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c447fffb900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c447fffb910: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c447fffb920: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c447fffb930: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==19316==ABORTING
```

