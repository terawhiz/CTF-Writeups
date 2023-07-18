# aush

tl;dr
- Stack buffer overflow of `0x200` on both inputs
- Overflow the envp variable in the stack which makes the execve of "Invalid username" cowsay fail and will overwrite password with our input
- Later Enter the correct password we overwrote and overflow envp with null bytes
- Execve now succeeds and we get a shell.

Exploit: [hack.py](./hack.py)\
Twitter: [ShuntIsReal](https://twitter.com/ShuntIsReal)