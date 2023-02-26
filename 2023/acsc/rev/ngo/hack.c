#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

// gcc new.c -g -o hack -lgmp

uint32_t seed = 0x3D2964F0;

uint64_t generate_random_number() {
    seed = seed >> 1 ^ -(seed & 1) & 0x80200003;
}

int main() {
    char flag[12] = { 1, 0x19, 0xef, 0x5a, 0xfa, 0xc8, 0x2e, 0x69, 0x31, 0xd7, 0x81, 0x21 };
    unsigned long v4 = 1;
    char num;
    char charr;
    int now = 0x2a;
    unsigned long temp = 1;
	printf("ACSC{");
    for (int i = 0; i <= 11; ++i) {
        for (unsigned int j = 0; j < v4 % (((uint64_t)1 << 32) - 1); ++j) {
            num = generate_random_number();
            // printf("v4 %% (((uint64_t)1 << 32) - 1) --> %ld\n", v4 % (((uint64_t)1 << 32) - 1));
        }
        charr = num ^ flag[i];
        printf("%c", charr);
        fflush(stdout);
        v4 *= now;
    }
    printf("}\n");
}

// ACSC{yUhFgRvQ2Afi}
