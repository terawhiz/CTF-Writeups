# bofww
```
buffer overflow with win function

nc bofww.2023.cakectf.com 9002
```
---
As the name challenge name implies this was an easy Stack buffer overflow pwn. The handout file contains a cpp source file, binary and dockerfiles. The binary was compiled with partial relro, no pie and canary. And there's a win function which gives a shell. Therefore now our goal is to control rip.

Reading the cpp source code we can find a stack buffer overflow on the `_name` variable in `input_person` function. The `std::cin` object accepts arbitrary amount of input until a white space or newline character is met.
```c
void input_person(int& age, std::string& name) {
  int _age;
  char _name[0x100];
  std::cout << "What is your first name? ";
  std::cin >> _name;
  ...
}
```

Providing a long input to the program we can see gdb crash in memmove libc function at `__memmove_avx_unaligned_erms+77` which copies a dword pointed by `rsi` register to the address pointed by `rdi`.
```gdb
 ► 0x7f89834069cd <__memmove_avx_unaligned_erms+77>  mov    word ptr [rdi + rdx - 2], si  <__stack_chk_fail@got.plt+1>
   0x7f89834069d2 <__memmove_avx_unaligned_erms+82>  mov    byte ptr [rdi], cl
   0x7f89834069d4 <__memmove_avx_unaligned_erms+84>  ret
```

Awesome, now we've acquired an arbitrary address write primitive. With this primitive we can write to any memory with writable permission set.
By overflowing the `_name` buffer we're damaging the stack canary so the `__stack_chk_fail` will be called before returning from `input_person` function. We could utilize it by writing win address to the `__stack_chk_fail` GOT entry.

Win function is called and we get a shell : )

When I solved the challenge I didn't really know why we're able to perform arbitrary write. Then later realized its because of `name = _name` instruction. Also thanks to someone in discord for giving a better explanation.

> [7:51 AM] IceCreamMan: At the end of the buffer overflow after the canary, there is an address to the string argument that was passed into the input_person function. The buffer overflow will overwrite that string to any target address, in this case the GOT of stack chk fail

There's a second part this challenge called `bofwow` where there's no win function. Read the challenge's writeup [here](../bofwow/)

Flag: `CakeCTF{n0w_try_w1th0ut_w1n_func710n:)}`
Exploit: [hack.py](./hack.py)