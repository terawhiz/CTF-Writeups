# bofwow
```
buffer overflow without win function

nc bofwow.2023.cakectf.com 9003
```
---
This is a writeup for second part of the challenge `bofww` and mostly focused on exploitation part. The bug is detailed in the other [writeup](../bofww/).


The win function has been removed in this challenge, but we've got onegadget. To use a onegadget libc base address is needed, but we don't have a libc address. How can we exploit this? This challenge can be solved without any leak by using a very powerful add-what-where primitive gadget.
```
0x00000000004012bc : add dword ptr [rbp - 0x3d], ebx ; nop ; ret
```


With the arbitrary write primitive overwrite `__stack_chk` GOT entry with `main` function address. Now the program is run again and again as long as the canary is changed in `input_person` function.

Perform stack pivoting and set rsp to bss section where we will be writing our rop chain. Our rop chain is pretty short.

1) Control `ebx` register contents. This gadget moves a dword pointed by `rbp-8` into `ebx` register. EBX will be added to the got entry of `setbuf` which will result in onegadget.
```
mov ebx, dword ptr [rbp - 8] ; leave ; ret
```
2) Perform 32bit addition on `ebx` to `[rbp-0x3d]` using the add-what-where gadget.
```
add dword ptr [rbp - 0x3d], ebx ; nop ; ret
```

Now the GOT entry of `setbuf` will contain our onegadget address.

3) Jump to `_start` or `setup` function which will eventually call the onegadget. And we get a shell!!


Flag: `CakeCTF{1_h3r3by_c3rt1fy_th4t_y0u_h4v3_c0mpl3ted_3very7h1ng_4b0ut_ROP}`

Exploit: [hack.py](./hack.py)