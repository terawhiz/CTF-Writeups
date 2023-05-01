#!/usr/bin/env python
from Crypto.Util.number import bytes_to_long, getPrime, isPrime, long_to_bytes
import random
import sys

encrypted_flag = 2583394315027752926476834450691881611079274871658465944538209888031229821550142438913873306275346246786172669929708244629961456581266389700761988149065305

def find_primes(rng):
    p = 0
    q = 0
    while p == q:
        while not isPrime(p):
            p = getPrime(256, randfunc=lambda n: rng.getrandbits(n).to_bytes((n+7)//8, 'big'))
        while not isPrime(q):
            q = getPrime(256, randfunc=lambda n: rng.getrandbits(n).to_bytes((n+7)//8, 'big'))    
    return p, q


def decrypt(enc, p, q, e=65537):
    n = p * q
    phi = (p - 1) * (q - 1)
    try:
        d = pow(e, -1, phi)
    except:
        return -1
    flag = pow(enc, d, n)
    flag = long_to_bytes(flag)
    return flag

# for seed in range(int(sys.argv[1]), int(sys.argv[2])):
for seed in range(624900000, 625000000):
    print(f"\r\rSeed = {seed}", end="")
    rng = random.Random(seed)
    p, q = find_primes(rng)

    flag = decrypt(encrypted_flag, p, q)
    if flag == -1:
        continue
    if b"BugBase{" in flag:
        print()
        print(flag)
        break

"""
Seed = 624995500
b'BugBase{n0rm4l_d1str1bu710n_f7w_1830572}'
"""