import numpy as np


def print_cups(current, cups):
    s = " ".join([str(c) if c != current else f"({c})" for c in cups])
    print(f"cups: {s}")


def play(current, cups):
    print_cups(current, cups)

    idx = cups.index(current)
    picks = [cups[i % len(cups)] for i in range(idx + 1, idx + 4)]
    print(f"pick up: " + ", ".join([str(c) for c in picks]))

    try:
        dest = sorted([c for c in cups if c not in picks and c < current])[::-1][0]
    except IndexError:
        dest = sorted([c for c in cups if c not in picks])[::-1][0]

    print(f"destination: {dest}")

    remaining = [c for c in cups if c not in picks]

    i = remaining.index(dest)
    cups = remaining[: i + 1] + picks + remaining[i + 1 :]

    new_idx = cups.index(current)
    cups = [cups[(i + new_idx - idx) % len(cups)] for i in range(len(cups))]

    return cups[(idx + 1) % len(cups)], cups


# Example label
label = "389125467"

# Puzzle input label
label = "167248359"

cups = [int(c) for c in label]
current = cups[0]

for i in range(100):
    print(f"\n-- move {i+1} --")
    current, cups = play(current, cups)

print("\n-- final --")
print_cups(current, cups)
idx = cups.index(1) + 1
part1 = "".join([str(cups[(idx + i) % len(cups)]) for i in range(len(cups) - 1)])
print(f"Part 1: {part1}")
