import time
from functools import cache


def parse(data):
    splitters = set()
    start = None
    w, h = len(data[0]), len(data)
    for (y, row) in enumerate(data):
        for (x, ch) in enumerate(row):
            if ch == 'S':
                start = (x, y)
            if ch == '^':
                splitters.add((x, y))

    return splitters, start, w, h

def print_manifold(w,h , splitters, all_beams, start):
    for y in range(h):
        row = ""
        for x in range(w):
            if (x, y) in all_beams:
                row += "|"
            elif (x, y) in splitters:
                row += "^"
            elif (x, y) == start:
                row += "S"
            else:
                row += "."
        print(row)




def part1(data, verbose=False):
    splitters, start, w, h = data
    print(f"W: {w} H: {h} Start: {start} Splitters: {len(splitters)}")

    all_beams = set()
    beams = set([start[0]])
    y = start[1] + 1

    split_count = 0

    while y < h:
        splits = set()
        dropped = set()
        for b in beams:
            if (b, y) in splitters:
                split_count += 1
                dropped.add(b)
                splits.add(b-1)
                splits.add(b+1)
        for b in dropped:
            beams.remove(b)
        for b in splits:
            beams.add(b)

        for b in beams:
            all_beams.add((b, y))
        # print_manifold(w, h, splitters, all_beams, start)
        # print("SPLIT COUNT: ", split_count)
        # input()

        y += 1

    return split_count


def part2(data, verbose=False):
    splitters, start, w, h = data

    @cache
    def rec(x, y):
        if y >= h:
            return 1

        if (x, y) in splitters:
            return rec(x+1, y + 1) + rec(x-1, y+1)
        else:
            return rec(x, y+1)

    return rec(*start)


def run(label, f):
    start = time.perf_counter()
    result = f()
    elapsed = time.perf_counter() - start
    if elapsed > 2:
        elapsed = f"{elapsed:.3f}s"
    else:
        elapsed = f"{elapsed*1000:.1f}ms"
    print(f"{label}: {result} ({elapsed})")


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

run("Part 1 with example data", lambda: part1(example, verbose=False))
run("Part 1 with real input", lambda: part1(lines, verbose=False))
run("Part 2 with example data", lambda: part2(example, verbose=False))
run("Part 2 with real input", lambda: part2(lines, verbose=False))
