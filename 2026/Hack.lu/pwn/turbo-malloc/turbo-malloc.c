#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>

#define MAGIC ((void*)0xf45735)
#define SIZE (1024*1024)
#define CHUNK_SIZE sizeof(struct chunk)
#define NUM_NOTES 16

struct chunk {
    struct chunk *next;
    size_t size;
    char memory[];
};

char memory[SIZE];
struct chunk *head;
bool first_request = true;

char *notes[NUM_NOTES] = { 0 };
unsigned long note_sizes[NUM_NOTES] = { 0 };

struct chunk* create_in_use_chunk(void *start, size_t size)
{
    struct chunk in_use_chunk = {
        .next = MAGIC,
        .size = size
    };
    memcpy(start, &in_use_chunk, CHUNK_SIZE);
    return (struct chunk*)start;
}

struct chunk* create_turbo_free_chunk(void *start, size_t size, struct chunk *next)
{
    struct chunk free_chunk = {
        .next = next,
        .size = size
    };
    memcpy(start, &free_chunk, CHUNK_SIZE);
    return (struct chunk*)start;
}

void *turbo_malloc (size_t size)
{
    if (size == 0) {
        return NULL;
    }

    // Align chunks to 16 bytes
    size = (size + 15) & -16;

    if (head == NULL) {
        // First time memory is used
        if (first_request == true) {
            first_request = false;

            struct chunk *in_use_chunk = create_in_use_chunk(memory, size);

            // If requested size is too large, turn chunk into turbo_free chunk
            if (size > (SIZE - CHUNK_SIZE)) {
                in_use_chunk->size = SIZE - CHUNK_SIZE;
                in_use_chunk->next = NULL;
                head = in_use_chunk;
                errno = ENOMEM;
                return NULL;
            }

            // If there is not/just enough space for a new header -> increase size of requested chunk
            if (size >= (SIZE - 2 * CHUNK_SIZE)) {
                in_use_chunk->size = SIZE - CHUNK_SIZE;
                head = NULL;
            } else {
                struct chunk *turbo_free_chunk = create_turbo_free_chunk(in_use_chunk->memory + in_use_chunk->size, SIZE - (CHUNK_SIZE * 2 + in_use_chunk->size), NULL);
                head = turbo_free_chunk;
            }

            return in_use_chunk->memory;

        // Program is out of memory
        } else {
            errno = ENOMEM;
            return NULL;
        }
    }

    struct chunk *current = head;
    struct chunk *prev = NULL;
    while (current != NULL) {
        if (size <= current->size) {
            // If there is not/just enough space for a new header -> increase size of requested chunk
            if ((current->size - size) <= CHUNK_SIZE) {
                // Edge case where head is the only turbo_free chunk
                if (current == head && current->next == NULL) {
                    head = NULL;
                //Edge case where head needs to be changed
                } else if (current == head) {
                    head = current->next;
                } else {
                    prev->next = current->next;
                }

                struct chunk* in_use_chunk = create_in_use_chunk(current, current->size);
                return in_use_chunk->memory;
            }

            void *turbo_free_chunk_start = (char*)current + CHUNK_SIZE + size;
            size_t turbo_free_chunk_size = current->size - CHUNK_SIZE - size;
            struct chunk* turbo_free_chunk = create_turbo_free_chunk(turbo_free_chunk_start, turbo_free_chunk_size, current->next);

            if (prev == NULL) {
                head = turbo_free_chunk;
            } else {
                prev->next = turbo_free_chunk;
            }

            struct chunk* in_use_chunk = create_in_use_chunk(current, size);
            return in_use_chunk->memory;
        }
        prev = current;
        current = current->next;
    }

    errno = ENOMEM;
    return NULL;
}

// Do not consolidate, turbo-heap must be blazingly fast!!!
void turbo_free (void *ptr)
{
    if (ptr == NULL) {
        return;
    }

    struct chunk *chunk = (struct chunk*)((char *)ptr - CHUNK_SIZE);

    if (chunk->next != MAGIC) {
        abort();
    }

    chunk->next = head;
    head = chunk;
    return;
}

void *turbo_realloc (void *ptr, size_t size)
{
    if (size == 0) {
        turbo_free(ptr);
        return NULL;
    }

    void *new_memory = turbo_malloc(size);
    if (new_memory == NULL) {
        return NULL;
    }

    if (ptr == NULL) {
        return new_memory;
    }

    struct chunk *chunk = (struct chunk*)((char *)ptr - CHUNK_SIZE);
    memcpy(new_memory, chunk->memory, chunk->size);
    turbo_free(ptr);

    return new_memory;
}

void die(const char *msg)
{
    perror(msg);
    exit(EXIT_FAILURE);
}

// just ignore this function
void init_buffering(void)
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

unsigned int get_note_slot()
{
    unsigned int note_slot = 0;
    printf("Slot (0-15): ");
    scanf("%u", &note_slot);
    getchar();

    if (note_slot >= NUM_NOTES) {
        puts("Please enter a number between 0 and 15!");
        exit(-1);
    }
    return note_slot;
}

int main(void)
{
    init_buffering();
    puts("----- Welcome to Turbo Notes -----");
    puts("1: Create a note");
    puts("2: Delete a note");
    puts("3: Read a note");
    puts("4: Write data to a note");
    puts("5: Expand a note");
    puts("6: Expand a note");
    puts("");

    unsigned int note_slot = 0;

    while (1) {
        printf("> ");
        unsigned int choice;
        if (!scanf("%u", &choice)) {
            getchar();
        }
 
        switch (choice) {
        case 1:
            note_slot = get_note_slot();
            if (notes[note_slot] != NULL) {
                puts("There already is a note at this index!");
                break;
            }

            printf("Size: ");
            scanf("%lu", &note_sizes[note_slot]);
            getchar();

            notes[note_slot] = turbo_malloc(note_sizes[note_slot]);

            if (notes[note_slot] == NULL) {
                die("turbo_malloc");
            }
            
            puts("Successfully created new note!");
            break;
        case 2:
            note_slot = get_note_slot();
            if(notes[note_slot] == NULL) {
                puts("No note at this index!");
                break;
            }

            turbo_free(notes[note_slot]);
            notes[note_slot] = NULL;
            note_sizes[note_slot] = 0;
            puts("Successfully deleted note!");
            break;
        case 3:
            note_slot = get_note_slot();
            if(notes[note_slot] == NULL) {
                puts("No note at this index!");
                break;
            }

            write(STDOUT_FILENO, notes[note_slot], note_sizes[note_slot]);
            break;
        case 4:
            note_slot = get_note_slot();
            if(notes[note_slot] == NULL) {
                puts("No note at this index!");
                break;
            }

            printf("Data: ");
            read(STDIN_FILENO, notes[note_slot], note_sizes[note_slot]);
            break;
        case 5:
            note_slot = get_note_slot();
            if(notes[note_slot] == NULL) {
                puts("No note at this index!");
                break;
            }

            unsigned long new_size;
            printf("New size: ");
            scanf("%lu", &new_size);
            getchar();

            notes[note_slot] = turbo_realloc(notes[note_slot], new_size);

            if (notes[note_slot] == NULL) {
                die("turbo_malloc");
            }

            note_sizes[note_slot] = new_size;

            puts("Successfully expanded note!");
            break;
        case 6:
            puts("Goodbye!");
            return 0;
        default:
            puts("Choice not recognized!");
            break;
        }
    }
}
