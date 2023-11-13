# vtable4b
```
Do you understand what vtable is?

nc vtable4b.2023.cakectf.com 9000
```
---

This was the most easiest pwn challenge in this ctf, easier than the Survey challenge.

tl;dr
- Craft a fake vtable with win function in the message buffer
- Overwrite vtable address with address of message buffer
- Then call the dialogue method to call win function

Flag: `CakeCTF{vt4bl3_1s_ju5t_4n_arr4y_0f_funct1on_p0int3rs}`

Exploit: [hack.py](./hack.py)