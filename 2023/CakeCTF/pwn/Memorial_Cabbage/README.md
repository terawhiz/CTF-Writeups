# Memorial Cabbage
```
Memorial Cabbage Unit 3

nc memorialcabbage.2023.cakectf.com 9001
```
---

In the challenge handout a binary, its c source and dockerfiles were provided.

There are two features in the program write memo and read memo. Write memo writes our message to a file at a temporary path and read memo reads the content of the file and displays it to the user.

The problem here is the use of `mkdtemp` function.
> The mkdtemp() function returns a pointer to the modified template string on success, and NULL on failure

A stack buffer is used as an argument to the function therefore `mkdtemp` returns a stack pointer. But the returned stack pointer is stored in `tempdir` pointer variable and used it across other two functions to read files.

We can overwrite the random directory buffer with `/flag.txt\x00` using the write memo feature. The calling read memo function the flag is printed on the screen.

Flag: `CakeCTF{B3_c4r3fuL_s0m3_libc_fuNcT10n5_r3TuRn_5t4ck_p01nT3r}`

Exploit: [hack.py](./hack.py)