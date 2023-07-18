# qjail

### tl;dr
- Stack Based Buffer Overflow in main function
- The program is run in a sandboxed environment using Qiling Framework
- Qiling maps the program and libc at a constant address
- The canary is always `0x6161616161616100`
- With the known information we can write a open, read and write rop chain to get the flag.

We can't get shell here because the rootfs only contain flag, challenge binary and libraries. And all the required information can be acquired from the debug output by setting `console=True`. GDB worked fine as a debugger with Qiling.

Exploit: [hack.py](./hack.py)\
Twitter: [ShuntIsReal](https://twitter.com/ShuntIsReal)