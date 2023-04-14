# traz - rev

The challenge author didn't provide any files to reverse except a netcat connection.


When connecting to the address we are greeted with a nice banner then the program gets some input from user. Spamming a bunch of A's we get the following error:

```
p00p: invalid instruction detected at 0x00
```

The error message suggests that the program runs custom VM which gets and executes VM code from the user. We can observe the program's behavior by passing random bytes as opcode.

Spam script:
```py
for i in range(0x100):
    p = remote("traz-1.play.hfsc.tf", 10101)
    p.recv()
    p.sendline(p8(i))
    p.recvuntil(b"p00p:\x1b[0m ")
    data = p.recv().strip()
    if b"invalid instruction" not in data:
        print(p8(i), "-->", data)
    p.close()
```

Output:
```
b'\x00' --> b'SIGSEGV detected at 0xff'
b'\x01' --> b'invalid register detected at 0x00'
b'\x02' --> b'invalid register detected at 0x00'
b'\x04' --> b'invalid register detected at 0x00'
b'\x08' --> b'invalid register detected at 0x00'
b'\x10' --> b'invalid register detected at 0x00'
b' '    --> b'SIGSEGV detected at 0xff'
b'@'    --> b'SIGSEGV detected at 0xff'
b'\x80' --> b'SIGSEGV detected at 0xff'
b'\xff' --> b'invalid register detected at 0x00'
```

The `0x1`, `0x2`, `0x4`, `0x8`, `0x10` and `0xff` opcodes expect register(s) as their arguments and some segfault. As we passed opcode without any operands which resulted in segfaults. After several attempts, we discovered that opcode 0x40 prints the entire state of the registers and memory from instruction 0x0 to 0xff

```c
-------- [DEBUG] --------

REG:
        A:     00     B:     00     C:     00
        D:     00     F:     00     PC:    ff

MEM:
        0x00:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x10:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x20:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x30:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x40:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x50:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x60:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x70:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x80:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0x90:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0xa0:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0xb0:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0xc0:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0xd0:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0xe0:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        0xf0:  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

With the help of powerfull spamtool (hands) we can get the following useful infomation which is very much enough to read any file from the server.

### **Instructions**:
|Instruction|Opcode|Arg1|Arg2|Explanation|
|-----------|------|----|----|--|
| imm | 0x1 |imm_val|register|Moves immediate value into a register|
|add|0x2|reg_src|reg_dest|Adds register values and stores in reg_dest|
|mov|0x4|reg_src|\[reg_dest\]|Moves register value into memory referenced by a register|

### **Registers**:
|Register|Value|
|-|-|
|A|0x1|
|B|0x2|
|C|0x4|
|D|0x8|
|F|0x10|

### **Syscalls**:
`0x80` is the syscall instruction and argument 2 decides what type of syscall should be executed.
|Syscall|arg2|
|-|-|
|open|0x1|
|read|0x2|
|write|0x4|
|sendfile|0x8|

With the above instruction we can read any files but what to read? where is the flag? guessed it would be in current directory and read `./flag` file. The orw operation was successful with open and sendfile instruction but contents of the file wasn't any useful.

### `./flag` contents:

```
the real flag file is somewhere else in the folder
```

Therefore I tried to leak the elf binary itself to see whats going on. We can get the elf path either with `/proc/self/cmdline` or can directly leak it with `/proc/self/exe`

By reversing the binary we can see the program first loading "boot.bin" into memory then it is executed later with `code_memory` as its argument. Here's the content of "boot.bin"

```
0x0000000000000000:  57                      push    rdi
0x0000000000000001:  31 C0                   xor     eax, eax
0x0000000000000003:  FF C0                   inc     eax
0x0000000000000005:  31 FF                   xor     edi, edi
0x0000000000000007:  FF C7                   inc     edi
0x0000000000000009:  48 C7 C6 00 71 33 01    mov     rsi, 0x1337100
0x0000000000000010:  48 C7 C2 10 00 00 00    mov     rdx, 0x10
0x0000000000000017:  0F 05                   syscall 
0x0000000000000019:  31 C0                   xor     eax, eax
0x000000000000001b:  31 FF                   xor     edi, edi
0x000000000000001d:  48 C7 C6 00 E0 0D 0C    mov     rsi, 0xc0de000
0x0000000000000024:  48 C7 C2 00 01 00 00    mov     rdx, 0x100
0x000000000000002b:  0F 05                   syscall 
0x000000000000002d:  5F                      pop     rdi
0x000000000000002e:  FF E7                   jmp     rdi
```


The program prints 0x10 bytes from `0x1337100` which is useless and the second syscall gets input (VM code) from user to `0xc0de000`.

**More reversing...**

There opcode `0x0` which we can use with `0x2` in `arg2` to load our shellcode into the `boot_memory@0x1337000` and execute `boot_memory` with the same opcode with  `arg2=1`. But there's a problem.

```c
ssize_t __fastcall read_shellcode@0x0148B(int a1)
{
  ssize_t result; // rax

  result = (unsigned __int8)how_to_set_you@0x06029 ^ 1u;
  if ( how_to_set_you@0x06029 == 1 )
    return read(a1, boot_memory, 0x1000uLL);
  return result;
}
```

Somehow we need to set a bit to `how_to_set_you@0x06029` variable to read in shellcode. Luckily there was an instruction (`opc = 0xff`) which will happily set a bit to the variable without exiting the program. From there we can send our shellcode and get a shell :)


Exploit: [Link](./exploit.py)

Flag: `midnight{b3t_y0U_c4nt_eX1t_V1M_th0}`