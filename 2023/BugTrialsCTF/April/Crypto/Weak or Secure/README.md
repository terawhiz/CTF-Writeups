# Weak or Secure - 100 Points

## Description:
```Our college professor has told us to design an encryption function using Python. However, one of my friends has designed a simple one. Could you please check if it is secure or not?```

## Solution:

Given a python program which opens `flag.txt` file, encrypts the text and prints them on the screen.


```py
def encrypt(message):
    alphabets="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~`!@#$%^&*()}{][|_"
    key = random.randint(1000,999999)
    enc = ""
    for letter in message:
        newpos=(alphabets.find(letter)+key)%len(alphabets)
        enc = enc + alphabets[newpos]
    return enc

text = encrypt(open('flag.txt','r').read())
print(text)
```

The `encrypt` function takes a `message` and encrypts using a simple substitution cipher. The function generates a random `key` between `1000 - 999999` using the `random` python module, and then shifts each letter in the message by the key value modulo the length of the alphabet.

We can easily solve this by bruteforcing the key.

**Solve script:**
```py
import random

encrypted_flag = "ha#h8|!3*GG&|7*H&J7K)7cJK&7J)~[e{NHG)2"
alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~`!@#$%^&*()}{][|_"

def decrypt(c, key):
    flag = ""
    for letter in c:
        newpos = (alphabets.find(letter)+key)%len(alphabets)
        flag = flag + alphabets[newpos]
    return flag

for i in range(1000, 999999):
    print(f"\r\rTrying: {i}", end="")
    flag = decrypt(encrypted_flag, i)
    if "BugBase" in flag:
        print()
        print(flag)
        break
```

Flag: `BugBase{l00ks_l1k3_4n_w34k_3ncryp710n}`