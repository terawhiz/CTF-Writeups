// Agile declassification tooling - don't tell anyone about our top secret project :]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>
#include <stdcountof.h>
#include <stdint.h>
#include <unistd.h>

static const char *const re = "flux";
static const char *const replace = "[REDACTED]";

static void die(const char *s) {
    perror(s);
    exit(EXIT_FAILURE);
}

static void redact(char buf[], size_t size) {
    const char *s = buf;
    regex_t regex;
    regmatch_t pmatch[1];
    regoff_t off, len;
    size_t remaining = size;

    if (regcomp(&regex, re, REG_NEWLINE))
        die("regcomp");

    for (unsigned int i = 0; ; i++) {
        if (regexec(&regex, s, countof(pmatch), pmatch, 0))
            break;

        off = pmatch[0].rm_so + (s - buf);
        len = pmatch[0].rm_eo - pmatch[0].rm_so;
        remaining = remaining - pmatch[0].rm_so - len;
        //printf("#%u:\n", i);
        //printf("rm_so = %d\n", pmatch[0].rm_so);
        //printf("rm_eo = %d\n", pmatch[0].rm_eo);
        //printf("remaining = %ld\n", remaining);
        //printf("offset = %jd; length = %jd\n", (intmax_t) off,
        //        (intmax_t) len);
        //printf("substring = \"%.*s\"\n", len, s + pmatch[0].rm_so);

        memcpy(&buf[off+strlen(replace)], &buf[off+len], remaining);
        memcpy(&buf[off], replace, strlen(replace));

        //printf("intermediate string: %s\n", buf);

        s += pmatch[0].rm_so + strlen(replace);
    }
}

int main(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    char buf[512] = { 0 };
    //fgets(buf, sizeof(buf), stdin);
    size_t n = read(STDIN_FILENO, buf, sizeof(buf));
    redact(buf, n);
    printf("%s", buf);
}
