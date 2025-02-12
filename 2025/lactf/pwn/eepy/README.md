# eepy

This was supposed to be a hard shellcoding challenge, but I cheesed it with execve syscall. Only 4 teams including us solved it, so I take this as a *tricky* challenge.

tl;dr solution:
- The `_start` function returns to the argc, so make args length to the address to our shellcode.
- Write very small `execve` shellcode, you utilize the ptr on the stack for commands.
- This is where I was stuck for 3 long hours because I was stupidly using spaces in the args. Do `cat$IFS*>/proc/1/fd/1` for the win.