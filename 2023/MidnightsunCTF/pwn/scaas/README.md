# scaas - pwn

The challenge is very simple, we have to pass 3 stages of 5 key checks so totally its 15 key checks. Then we can send our shellcode to get a shell, but the shellcode can only contain Alphanumeric characters. We can steal the shellcode online which will give us a shell.

Exploit: [link](./exp.py)

Flag: `midnight{m0d3rn_cl0ud_sh3llc0de5}`