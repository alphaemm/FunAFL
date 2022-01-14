

# Invalid write in function t2p_readwrite_pdf_image at tiff2pdf.c:2536 and Invalid read in function t2p_writeproc at tiff2pdf.c:415

Tested in Ubuntu 16.04, 64bit.

The testcase is [Invaild_write_and_read](Invaild_write_and_read).

I use the following command:

```
./tiff2pdf Invaild_write_and_read -o /dev/null
```

and get:

```
TIFFReadDirectoryCheckOrder: Warning, Invalid TIFF directory; tags are not sorted in ascending order.
TIFFReadDirectory: Warning, Unknown field with tag 1 (0x1) encountered.
TIFFReadDirectory: Warning, Unknown field with tag 15 (0xf) encountered.
TIFFFetchNormalTag: Warning, ASCII value for tag "DocumentName" does not end in null byte.
_TIFFVSetField: Invaild_write_and_read: Bad value 6682 for "Orientation" tag.
TIFFReadDirectory: Warning, TIFF directory is missing required "StripByteCounts" field, calculating from imagelength.
TIFFAdvanceDirectory: Error fetching directory count.
TIFFReadDirectoryCheckOrder: Warning, Invalid TIFF directory; tags are not sorted in ascending order.
TIFFReadDirectory: Warning, Unknown field with tag 1 (0x1) encountered.
TIFFReadDirectory: Warning, Unknown field with tag 15 (0xf) encountered.
TIFFFetchNormalTag: Warning, ASCII value for tag "DocumentName" does not end in null byte.
_TIFFVSetField: Invaild_write_and_read: Bad value 6682 for "Orientation" tag.
TIFFReadDirectory: Warning, TIFF directory is missing required "StripByteCounts" field, calculating from imagelength.
TIFFReadDirectoryCheckOrder: Warning, Invalid TIFF directory; tags are not sorted in ascending order.
TIFFReadDirectory: Warning, Unknown field with tag 1 (0x1) encountered.
TIFFReadDirectory: Warning, Unknown field with tag 15 (0xf) encountered.
TIFFFetchNormalTag: Warning, ASCII value for tag "DocumentName" does not end in null byte.
_TIFFVSetField: Invaild_write_and_read: Bad value 6682 for "Orientation" tag.
TIFFReadDirectory: Warning, TIFF directory is missing required "StripByteCounts" field, calculating from imagelength.
TIFFReadDirectoryCheckOrder: Warning, Invalid TIFF directory; tags are not sorted in ascending order.
TIFFReadDirectory: Warning, Unknown field with tag 1 (0x1) encountered.
TIFFReadDirectory: Warning, Unknown field with tag 15 (0xf) encountered.
TIFFFetchNormalTag: Warning, ASCII value for tag "DocumentName" does not end in null byte.
_TIFFVSetField: Invaild_write_and_read: Bad value 6682 for "Orientation" tag.
TIFFReadDirectory: Warning, TIFF directory is missing required "StripByteCounts" field, calculating from imagelength.
*** Error in `./tiff2pdf': free(): invalid size: 0x0000000001c95ee0 ***
======= Backtrace: =========
/lib/x86_64-linux-gnu/libc.so.6(+0x777f5)[0x7fae26b197f5]
/lib/x86_64-linux-gnu/libc.so.6(+0x8038a)[0x7fae26b2238a]
/lib/x86_64-linux-gnu/libc.so.6(cfree+0x4c)[0x7fae26b2658c]
./tiff2pdf[0x419788]
./tiff2pdf[0x430440]
./tiff2pdf[0x402cd0]
/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf0)[0x7fae26ac2840]
./tiff2pdf[0x403209]
======= Memory map: ========
00400000-00436000 r-xp 00000000 103:01 22502786                          ./tiff2pdf
00635000-00636000 r--p 00035000 103:01 22502786                          ./tiff2pdf
00636000-00637000 rw-p 00036000 103:01 22502786                          ./tiff2pdf
01c91000-01cb2000 rw-p 00000000 00:00 0                                  [heap]
7fae20000000-7fae20021000 rw-p 00000000 00:00 0 
7fae20021000-7fae24000000 ---p 00000000 00:00 0 
7fae25ada000-7fae25af1000 r-xp 00000000 103:01 10504621                  /lib/x86_64-linux-gnu/libgcc_s.so.1
7fae25af1000-7fae25cf0000 ---p 00017000 103:01 10504621                  /lib/x86_64-linux-gnu/libgcc_s.so.1
7fae25cf0000-7fae25cf1000 r--p 00016000 103:01 10504621                  /lib/x86_64-linux-gnu/libgcc_s.so.1
7fae25cf1000-7fae25cf2000 rw-p 00017000 103:01 10504621                  /lib/x86_64-linux-gnu/libgcc_s.so.1
7fae25cf2000-7fae25cf5000 r-xp 00000000 103:01 10491303                  /lib/x86_64-linux-gnu/libdl-2.23.so
7fae25cf5000-7fae25ef4000 ---p 00003000 103:01 10491303                  /lib/x86_64-linux-gnu/libdl-2.23.so
7fae25ef4000-7fae25ef5000 r--p 00002000 103:01 10491303                  /lib/x86_64-linux-gnu/libdl-2.23.so
7fae25ef5000-7fae25ef6000 rw-p 00003000 103:01 10491303                  /lib/x86_64-linux-gnu/libdl-2.23.so
7fae25ef6000-7fae25ffe000 r-xp 00000000 103:01 10491309                  /lib/x86_64-linux-gnu/libm-2.23.so
7fae25ffe000-7fae261fd000 ---p 00108000 103:01 10491309                  /lib/x86_64-linux-gnu/libm-2.23.so
7fae261fd000-7fae261fe000 r--p 00107000 103:01 10491309                  /lib/x86_64-linux-gnu/libm-2.23.so
7fae261fe000-7fae261ff000 rw-p 00108000 103:01 10491309                  /lib/x86_64-linux-gnu/libm-2.23.so
7fae261ff000-7fae26218000 r-xp 00000000 103:01 10486643                  /lib/x86_64-linux-gnu/libz.so.1.2.8
7fae26218000-7fae26417000 ---p 00019000 103:01 10486643                  /lib/x86_64-linux-gnu/libz.so.1.2.8
7fae26417000-7fae26418000 r--p 00018000 103:01 10486643                  /lib/x86_64-linux-gnu/libz.so.1.2.8
7fae26418000-7fae26419000 rw-p 00019000 103:01 10486643                  /lib/x86_64-linux-gnu/libz.so.1.2.8
7fae26419000-7fae26470000 r-xp 00000000 103:01 14813331                  /usr/lib/x86_64-linux-gnu/libjpeg.so.8.0.2
7fae26470000-7fae26670000 ---p 00057000 103:01 14813331                  /usr/lib/x86_64-linux-gnu/libjpeg.so.8.0.2
7fae26670000-7fae26671000 r--p 00057000 103:01 14813331                  /usr/lib/x86_64-linux-gnu/libjpeg.so.8.0.2
7fae26671000-7fae26672000 rw-p 00058000 103:01 14813331                  /usr/lib/x86_64-linux-gnu/libjpeg.so.8.0.2
7fae26672000-7fae2667d000 r-xp 00000000 103:01 14819829                  /usr/lib/x86_64-linux-gnu/libjbig.so.0
7fae2667d000-7fae2687c000 ---p 0000b000 103:01 14819829                  /usr/lib/x86_64-linux-gnu/libjbig.so.0
7fae2687c000-7fae2687d000 r--p 0000a000 103:01 14819829                  /usr/lib/x86_64-linux-gnu/libjbig.so.0
7fae2687d000-7fae26880000 rw-p 0000b000 103:01 14819829                  /usr/lib/x86_64-linux-gnu/libjbig.so.0
7fae26880000-7fae268a1000 r-xp 00000000 103:01 10490493                  /lib/x86_64-linux-gnu/liblzma.so.5.0.0
7fae268a1000-7fae26aa0000 ---p 00021000 103:01 10490493                  /lib/x86_64-linux-gnu/liblzma.so.5.0.0
7fae26aa0000-7fae26aa1000 r--p 00020000 103:01 10490493                  /lib/x86_64-linux-gnu/liblzma.so.5.0.0
7fae26aa1000-7fae26aa2000 rw-p 00021000 103:01 10490493                  /lib/x86_64-linux-gnu/liblzma.so.5.0.0
7fae26aa2000-7fae26c62000 r-xp 00000000 103:01 10491305                  /lib/x86_64-linux-gnu/libc-2.23.so
7fae26c62000-7fae26e62000 ---p 001c0000 103:01 10491305                  /lib/x86_64-linux-gnu/libc-2.23.so
7fae26e62000-7fae26e66000 r--p 001c0000 103:01 10491305                  /lib/x86_64-linux-gnu/libc-2.23.so
7fae26e66000-7fae26e68000 rw-p 001c4000 103:01 10491305                  /lib/x86_64-linux-gnu/libc-2.23.so
7fae26e68000-7fae26e6c000 rw-p 00000000 00:00 0 
7fae26e6c000-7fae2703f000 r-xp 00000000 103:01 22502764                  /path-to-install/lib/libtiff.so.5.5.0
7fae2703f000-7fae2723e000 ---p 001d3000 103:01 22502764                  /path-to-install/lib/libtiff.so.5.5.0
7fae2723e000-7fae27242000 r--p 001d2000 103:01 22502764                  /path-to-install/lib/libtiff.so.5.5.0
7fae27242000-7fae27243000 rw-p 001d6000 103:01 22502764                  /path-to-install/lib/libtiff.so.5.5.0
7fae27243000-7fae27244000 rw-p 00000000 00:00 0 
7fae27244000-7fae2726a000 r-xp 00000000 103:01 10491316                  /lib/x86_64-linux-gnu/ld-2.23.so
7fae27434000-7fae27439000 rw-p 00000000 00:00 0 
7fae27466000-7fae27467000 rw-p 00000000 00:00 0 
7fae27467000-7fae27468000 r--s 00000000 103:01 22416645                  ./Invaild_write_and_read
7fae27468000-7fae27469000 rw-p 00000000 00:00 0 
7fae27469000-7fae2746a000 r--p 00025000 103:01 10491316                  /lib/x86_64-linux-gnu/ld-2.23.so
7fae2746a000-7fae2746b000 rw-p 00026000 103:01 10491316                  /lib/x86_64-linux-gnu/ld-2.23.so
7fae2746b000-7fae2746c000 rw-p 00000000 00:00 0 
7ffff981d000-7ffff983f000 rw-p 00000000 00:00 0                          [stack]
7ffff9943000-7ffff9946000 r--p 00000000 00:00 0                          [vvar]
7ffff9946000-7ffff9948000 r-xp 00000000 00:00 0                          [vdso]
ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]
Aborted (core dumped)
```

I use **valgrind** to analysis the bug and get the below information (absolute path information omitted):

```
==11534== Memcheck, a memory error detector
==11534== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
==11534== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
==11534== Command: ./tiff2pdf Invaild_write_and_read -o /dev/null
==11534== 
--11534-- WARNING: Serious error when reading debug info
--11534-- When reading debug info from /lib/x86_64-linux-gnu/libz.so.1.2.8:
--11534-- Ignoring non-Dwarf2/3/4 block in .debug_info
--11534-- WARNING: Serious error when reading debug info
--11534-- When reading debug info from /lib/x86_64-linux-gnu/libz.so.1.2.8:
--11534-- Last block truncated in .debug_info; ignoring
--11534-- WARNING: Serious error when reading debug info
--11534-- When reading debug info from /lib/x86_64-linux-gnu/libz.so.1.2.8:
--11534-- parse_CU_Header: is neither DWARF2 nor DWARF3 nor DWARF4
TIFFReadDirectoryCheckOrder: Warning, Invalid TIFF directory; tags are not sorted in ascending order.
TIFFReadDirectory: Warning, Unknown field with tag 1 (0x1) encountered.
TIFFReadDirectory: Warning, Unknown field with tag 15 (0xf) encountered.
TIFFFetchNormalTag: Warning, ASCII value for tag "DocumentName" does not end in null byte.
_TIFFVSetField: Invaild_write_and_read: Bad value 6682 for "Orientation" tag.
TIFFReadDirectory: Warning, TIFF directory is missing required "StripByteCounts" field, calculating from imagelength.
TIFFAdvanceDirectory: Error fetching directory count.
TIFFReadDirectoryCheckOrder: Warning, Invalid TIFF directory; tags are not sorted in ascending order.
TIFFReadDirectory: Warning, Unknown field with tag 1 (0x1) encountered.
TIFFReadDirectory: Warning, Unknown field with tag 15 (0xf) encountered.
TIFFFetchNormalTag: Warning, ASCII value for tag "DocumentName" does not end in null byte.
_TIFFVSetField: Invaild_write_and_read: Bad value 6682 for "Orientation" tag.
TIFFReadDirectory: Warning, TIFF directory is missing required "StripByteCounts" field, calculating from imagelength.
TIFFReadDirectoryCheckOrder: Warning, Invalid TIFF directory; tags are not sorted in ascending order.
TIFFReadDirectory: Warning, Unknown field with tag 1 (0x1) encountered.
TIFFReadDirectory: Warning, Unknown field with tag 15 (0xf) encountered.
TIFFFetchNormalTag: Warning, ASCII value for tag "DocumentName" does not end in null byte.
_TIFFVSetField: Invaild_write_and_read: Bad value 6682 for "Orientation" tag.
TIFFReadDirectory: Warning, TIFF directory is missing required "StripByteCounts" field, calculating from imagelength.
TIFFReadDirectoryCheckOrder: Warning, Invalid TIFF directory; tags are not sorted in ascending order.
TIFFReadDirectory: Warning, Unknown field with tag 1 (0x1) encountered.
TIFFReadDirectory: Warning, Unknown field with tag 15 (0xf) encountered.
TIFFFetchNormalTag: Warning, ASCII value for tag "DocumentName" does not end in null byte.
_TIFFVSetField: Invaild_write_and_read: Bad value 6682 for "Orientation" tag.
TIFFReadDirectory: Warning, TIFF directory is missing required "StripByteCounts" field, calculating from imagelength.
==11534== Invalid write of size 1
==11534==    at 0x41975E: t2p_readwrite_pdf_image (tiff2pdf.c:2536)
==11534==    by 0x43043F: t2p_write_pdf (tiff2pdf.c:5709)
==11534==    by 0x402CCF: main (tiff2pdf.c:827)
==11534==  Address 0x639ef37 is 0 bytes after a block of size 3,063 alloc'd
==11534==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==11534==    by 0x415A88: t2p_readwrite_pdf_image (tiff2pdf.c:2476)
==11534==    by 0x43043F: t2p_write_pdf (tiff2pdf.c:5709)
==11534==    by 0x402CCF: main (tiff2pdf.c:827)
==11534== 
==11534== Invalid write of size 1
==11534==    at 0x419771: t2p_readwrite_pdf_image (tiff2pdf.c:2537)
==11534==    by 0x43043F: t2p_write_pdf (tiff2pdf.c:5709)
==11534==    by 0x402CCF: main (tiff2pdf.c:827)
==11534==  Address 0x639ef38 is 1 bytes after a block of size 3,063 alloc'd
==11534==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==11534==    by 0x415A88: t2p_readwrite_pdf_image (tiff2pdf.c:2476)
==11534==    by 0x43043F: t2p_write_pdf (tiff2pdf.c:5709)
==11534==    by 0x402CCF: main (tiff2pdf.c:827)
==11534== 
==11534== Invalid read of size 1
==11534==    at 0x4C35078: __GI_mempcpy (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==11534==    by 0x528B251: _IO_file_xsputn@@GLIBC_2.2.5 (fileops.c:1319)
==11534==    by 0x52807CA: fwrite (iofwrite.c:39)
==11534==    by 0x4039A0: t2p_writeproc (tiff2pdf.c:415)
==11534==    by 0x41977F: t2p_readwrite_pdf_image (tiff2pdf.c:2538)
==11534==    by 0x43043F: t2p_write_pdf (tiff2pdf.c:5709)
==11534==    by 0x402CCF: main (tiff2pdf.c:827)
==11534==  Address 0x639ef37 is 0 bytes after a block of size 3,063 alloc'd
==11534==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==11534==    by 0x415A88: t2p_readwrite_pdf_image (tiff2pdf.c:2476)
==11534==    by 0x43043F: t2p_write_pdf (tiff2pdf.c:5709)
==11534==    by 0x402CCF: main (tiff2pdf.c:827)
==11534== 
==11534== Invalid read of size 1
==11534==    at 0x4C35086: __GI_mempcpy (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==11534==    by 0x528B251: _IO_file_xsputn@@GLIBC_2.2.5 (fileops.c:1319)
==11534==    by 0x52807CA: fwrite (iofwrite.c:39)
==11534==    by 0x4039A0: t2p_writeproc (tiff2pdf.c:415)
==11534==    by 0x41977F: t2p_readwrite_pdf_image (tiff2pdf.c:2538)
==11534==    by 0x43043F: t2p_write_pdf (tiff2pdf.c:5709)
==11534==    by 0x402CCF: main (tiff2pdf.c:827)
==11534==  Address 0x639ef38 is 1 bytes after a block of size 3,063 alloc'd
==11534==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==11534==    by 0x415A88: t2p_readwrite_pdf_image (tiff2pdf.c:2476)
==11534==    by 0x43043F: t2p_write_pdf (tiff2pdf.c:5709)
==11534==    by 0x402CCF: main (tiff2pdf.c:827)
==11534== 
==11534== 
==11534== HEAP SUMMARY:
==11534==     in use at exit: 0 bytes in 0 blocks
==11534==   total heap usage: 112 allocs, 112 frees, 75,927 bytes allocated
==11534== 
==11534== All heap blocks were freed -- no leaks are possible
==11534== 
==11534== For counts of detected and suppressed errors, rerun with: -v
==11534== ERROR SUMMARY: 4 errors from 4 contexts (suppressed: 0 from 0)
```

An attacker can exploit this vulnerability by submitting a malicious bmp that exploits this bug which will result in a Denial of Service (DoS).

