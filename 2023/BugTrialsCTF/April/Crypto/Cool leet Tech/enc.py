import random
from tqdm import tqdm
from Crypto.Util.number import bytes_to_long, getPrime, isPrime

def rng_initializer():
    seed = 0
    for i in tqdm(range(1000000000)):
        seed += random.randint(0, random.randint(0, random.randint(0, random.randint(0, 10))))
    print(f"{seed=}")
    rng = random.Random(seed)
    return rng


def find_primes(rng):
    p = 0
    q = 0
    while p == q:
        while not isPrime(p):
            p = getPrime(256, randfunc=lambda n: rng.getrandbits(n).to_bytes((n+7)//8, 'big'))
        while not isPrime(q):
            q = getPrime(256, randfunc=lambda n: rng.getrandbits(n).to_bytes((n+7)//8, 'big'))    
    return p, q


def encrypt(m: bytes, p: int, q: int, e: int) -> int:
    n = p * q
    m = bytes_to_long(m)
    enc = pow(m, e, n)
    return enc


if __name__ == '__main__':
    rng = rng_initializer()
    p, q = find_primes(rng)
    print(f"{p=}, {q=}")
    e = 65537
    flag = open('flag.txt', 'rb').read()
    enc = encrypt(flag, p, q, e)
    print(f"{enc=}")
    # with open("output.txt", "w") as f:
    #     f.write(f"{enc=}")