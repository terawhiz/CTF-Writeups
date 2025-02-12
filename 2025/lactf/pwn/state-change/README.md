# state-change

tl;dr
- 0x10 bytes stack buffer overflow
- Pivot to bss, overwrite the state variable
- Then ret2win