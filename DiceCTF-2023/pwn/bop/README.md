# bop

Given 64 bit ELF binary with no pie or stack canary. The vulnerability was in the main function stack buffer overflow via gets function call. Since NX bit is enabled we can't run shelllcode directly on stack. So we have to ROP and get the flag.

Note: We can't get a shell here because of seccomp. Allowed syscalls are read, write, open, exit, and exit_group

We can use orw syscalls to read the flag file. Flag file location is mentioned in the Dockerfile. (Its /app/flag.txt not /srv/app/flag.txt because that's how pwn.red jails work)

### ROP chain:

- Write a format string to bss using gets then pass its address as an argument to printf to leak libc address.
- Read payload into bss region. Pivot to bss
- write flag path to bss
- Got syscall gadget from libc. Then perform orw to get the flag.
- make sure to exit cleanly :)

[Link](./hack.py) to exploit

##### Acknowledgements:

- JoshL#4217 posted half of the solve script
- Often username changing person raced to solve this challenge before I did 😄
