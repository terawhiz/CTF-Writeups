#include "zephyr/fatal.h"
#include <zephyr/kernel.h>

#include <xtensa/simcall.h>
#include <zephyr/logging/log_ctrl.h>
#include <zephyr/sys/printk.h>

/* Defined in lib/libc/picolibc/stdio.c */
void __stdin_hook_install(unsigned char (*hook)(void));
/* Defined in drivers/console/xtensa_sim_console.c */
int arch_printk_char_out(int c);

/* Read one byte via semihosting (simcall) from the QEMU console */
static unsigned char sim_console_getc(void) {
    char c;

    for (;;) {
        register int a2 __asm__("a2") = SYS_read;
        register int a3 __asm__("a3") = 0; /* fd 0 = stdin */
        register char *a4 __asm__("a4") = &c;
        register int a5 __asm__("a5") = 1;

        __asm__ volatile("simcall"
                         : "+a"(a2), "+a"(a3)
                         : "a"(a4), "a"(a5)
                         : "memory");
        if (a2 == 1) {
            break;
        }
        k_msleep(10);
    }

    /* Terminal in raw mode: Enter sends CR */
    if (c == '\r') {
        c = '\n';
    }
    arch_printk_char_out(c);
    return (unsigned char)c;
}

void read_line(char *buffer, size_t n) {
    int read = 0;
    while (n - read > 0) {
        int c = getchar();
        if (c == EOF) {
            printk("error reading\n");
            k_fatal_halt(0);
        } else if (c == '\n') {
            buffer[read] = 0;
            return;
        }
        buffer[read++] = c;
    }
}

void echo(void) {
    char buf[16];
    printk("Enter message to echo: ");
    read_line(buf, 128);
    printk("\nmessage: %s\n", buf);
}

int menu(void) {
    char buf[16];
    printk("Choose option:\n1: echo message\n2: exit\n");
    read_line(buf, sizeof(buf));
    if (buf[0] == '1') {
        echo();
    } else if (buf[0] == '2') {
        return 1;
    } else {
        printk("Unknown command\n");
    }
    return 0;
}

void echo_server(void) {
    int ret = 0;
    while (!ret) {
        ret = menu();
    }
    printk("Goodbye\n");
}

int main(void) {
    // connect console input to stdin, zephyr doesn't do it by default
    __stdin_hook_install(sim_console_getc);

    echo_server();
    k_fatal_halt(255);
    return 0;
}
