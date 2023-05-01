#!/usr/bin/env python
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

'''
Output:

ha#h8|!3*GG&|7*H&J7K)7cJK&7J)~[e{NHG)2
'''

# BugBase{l00ks_l1k3_4n_w34k_3ncryp710n}