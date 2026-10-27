# turbo-malloc

Out of bounds write in realloc. It uses old size to memcpy data into new chunk. Use the oob to overwrite the next pointer on a free chunk, leak libc pointer, change stderr ptr to a forged stderr to do FSOP.