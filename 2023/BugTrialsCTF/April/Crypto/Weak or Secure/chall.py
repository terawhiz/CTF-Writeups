import random

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

'''
Output:

ha#h8|!3*GG&|7*H&J7K)7cJK&7J)~[e{NHG)2
'''