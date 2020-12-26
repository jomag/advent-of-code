
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>

#define VERBOSE 0

#if VERBOSE
const uint32_t CUP_COUNT = 9;
const uint32_t PICK_COUNT = 3;
const uint32_t MOVE_COUNT = 10;
#else
const uint32_t CUP_COUNT = 1000000;
const uint32_t PICK_COUNT = 3;
const uint32_t MOVE_COUNT = 10000000;
#endif

static uint32_t buf1[CUP_COUNT];
static uint32_t buf2[CUP_COUNT];
static uint32_t *cups = buf1;
static uint32_t *cups_next = buf2;

void print_cups(uint32_t* cupv, size_t count)
{
    static char buf[1024];
    char *s = buf;

    for (int i = 0; i < count && i < 20; i++) {
        if (i == 0) {
            s += sprintf(s, "(%u) ", cupv[i]);
        } else {
            s += sprintf(s, "%u ", cupv[i]);
        }
    }

    printf("cups: %s\n", buf);
}

void play()
{
    uint32_t picks[3];
    uint32_t current_value;
    uint32_t dest;
    uint32_t tmp;

#if VERBOSE
    print_cups(cups, CUP_COUNT);
#endif 

    // 1. The crab picks up *three cups* that are immediately *clockwise*
    //    of the *current cup*. They are removed from the circle; cup spacing
    //    is adjusted as necessary to maintain the circle.
    for (uint32_t i = 0; i < PICK_COUNT; i++) {
        picks[i] = cups[(1 + i) % CUP_COUNT];
    }

#if VERBOSE
    printf("pick up: %d, %d, %d\n", picks[0], picks[1], picks[2]);
#endif

    current_value = cups[0];

    // 2. The crab selects a *destination cup*: the cup with a *label* equal to
    //    the *current cup's* label minus one. If this would select one of the
    //    cups that was just picked up, the crab will keep subtracting one until
    //    it finds a cup that wasn't just picked up. If at any point in this
    //    process the value goes below the lowest value on any cup's label,
    //    it *wraps around* to the highest value on any cup's label instead.
    dest = current_value;
    bool found = false;
    while (!found) {
        found = true;

        if (dest == 1) {
            dest = CUP_COUNT;
        } else {
            dest--;
        }

        for (uint32_t i = 0; i < PICK_COUNT; i++) {
            if (picks[i] == dest) {
                found = false;
            }
        }
    }

#if VERBOSE
    printf("destination: %d\n", dest);
#endif

    // 3. The crab places the cups it just picked up so that they are *immediately
    //    clockwise* of the destination cup. They keep the same order as when they
    //    were picked up.

    // Example cups: IDX P1 P2 P3    A   B   C  DST D  E   F
    //               0   1  2  3     4   5   6  7   8  9  10
    //               A   B  C  DST  P1  P2  P3  D   E  F IDX

    // Search for index of destination cup (start at 4'th)
    size_t dest_index = CUP_COUNT - 1;
    while (cups[dest_index] != dest) {
        dest_index--;
    }

    // Store current index
    tmp = cups[0];

    // Copy everyting up to and including the index cup to next buffer,
    // but leave out the index cup and the three picked cups.
    memcpy(
        cups_next,
        cups + 1 + PICK_COUNT,
        (dest_index - 3) * sizeof(uint32_t)
    );

    // Place picks after destination cup
    memcpy(
        cups_next + dest_index - 3,
        picks,
        PICK_COUNT * sizeof(uint32_t)
    );

    // Copy everything following the destination cup
    memcpy(
        cups_next + dest_index,
        cups + dest_index + 1,
        (CUP_COUNT - dest_index - 1) * sizeof(uint32_t)
    );

    // Finally, place the index last
    cups_next[CUP_COUNT - 1] = tmp;

    // Swap buffers
    uint32_t *p = cups;
    cups = cups_next;
    cups_next = p;
}

void init()
{
#if VERBOSE
    uint32_t label[] = { 3, 8, 9, 1, 2, 5, 4, 6, 7 };
#else
    uint32_t label[] = { 1, 6, 7, 2, 4, 8, 3, 5, 9 };
#endif

    for (uint32_t i = 0; i < CUP_COUNT; i++) {
        cups[i] = i + 1;
    }
    memcpy(cups, label, sizeof(label));
}

int main(int argc, char *argv[]) {
    init();

    for (uint32_t i = 0; i < MOVE_COUNT + 3; i++) {
#if VERBOSE
        fgetc(stdin);
        printf("-- move %d --\n", i + 1);
#else
        if (i % 1000 == 0) {
            printf("move %d ...\n", i);
        }
#endif
        play();

        if (i > MOVE_COUNT - 6) {
            printf("At move %d:\n", i);
            for (uint32_t i = 0; i < CUP_COUNT; i++) {
                if (cups[i] == 1) {
                    uint64_t a = cups[(i + 1) % CUP_COUNT];
                    uint64_t b = cups[(i + 2) % CUP_COUNT];
                    printf("Part 2: %ld * %ld = %ld\n", a, b, a * b);
                    break;
                }
            }
        }
    }

    for (uint32_t i = 0; i < CUP_COUNT; i++) {
        if (cups[i] == 1) {
            uint64_t a = cups[(i + 1) % CUP_COUNT];
            uint64_t b = cups[(i + 2) % CUP_COUNT];
            printf("Part 2: %ld * %ld = %ld\n", a, b, a * b);
            break;
        }
    }

    return 0;
}


// Wrong guesses: too low - Part 2: 141014 * 155917 = 511643358