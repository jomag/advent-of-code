#include <stdint.h>
#include <stdio.h>

int64_t run(int64_t inp[]) {
    int64_t x = 0;
    int z = 0;

    for (int i = 0; i < 14; i++) {
        // Digit 0..4
        z = 2024920 + inp[0] * 456976 + inp[1] * 17576 + inp[2] * 676 + inp[3] * 26 + inp[4];

        // Digit 5
        x = z % 26 - 10;
        z = z / 26;
        if (x != inp[5]) {
            z = 26 * z + inp[5] + 7;
        }

        // Digit 6
        z = 26 * z + inp[6] + 11;

        // Digit 7
        x = z % 26 - 9;
        z = z / 26;
        if (x != inp[7]) {
            z = 26 * z + inp[7] + 4;
        }

        // Digit 8
        x = z % 26 - 3;
        z = z / 26;
        if (x != inp[8]) {
            z = 26 * z + inp[8] + 6;
        }

        // Digit 9
        z = 26 * z + inp[9] + 5;

        // Digit 10
        x = z % 26 - 5;
        z = z / 26;
        if (x != inp[10]) {
            z = 26 * z + inp[10] + 9;
        }

        // Digit 11
        x = z % 26 - 10;
        z = z / 26;
        if (x != inp[11]) {
            z = 26 * z + inp[11] + 12;
        }

        // Digit 12
        x = z % 26 - 4;
        z = z / 26;
        if (x != inp[12]) {
            z = 26 * z + inp[12] + 14;
        }

        // Digit 13
        x = z % 26 - 5;
        z = z / 26;
        if (x != inp[13]) {
            z = 26 * z + inp[13] + 14;
        }
    }

    return z;
}

void print_input(int64_t inp[]) {
    for (int n = 0; n < 14; n++) {
        printf("%lld ", inp[n]);
    }
    printf("\n");
}

int main(int argc, char *argv[]) {
    // [8, 2, 8, 1, 6, 2, 1, 3, 5, 3, 1, 7, 9, 8] -> vm: 148754108, algo: 148754108
    int64_t inp[14] = {9,9,9,9,9,9,9,9,9,9,9,9,9,9};
    int step = 0;

    while (1) {
        if (step % 100000 == 0) {
            print_input(inp);
        }
        step++;


        for (int n = 13; n >= 0; n--) {
            if (inp[n] > 1) {
                inp[n] -= 1;
                break;
            } else {
                inp[n] = 9;
            }
        }

        int64_t z = run(inp);
        if (z == 0) {
            printf("Found it! z=%lld\n", z);
            print_input(inp);
        }
    }
}