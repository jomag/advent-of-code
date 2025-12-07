import sys
import time
from itertools import combinations


def parse(data):
    ranges = set()
    ingr = set()
    m = 0
    for line in data:
        if line == "":
            m = 1
            continue
        if m == 0:
            a, b = line.split("-")
            ranges.add((int(a), int(b)))
        else:
            ingr.add(int(line))

    return ranges, ingr


def part1(data, verbose=False):
    ranges, ingr = data

    def is_fresh(x):
        for a, b in ranges:
            if a <= x and b >= x:
                return True
        return False

    tot = 0
    for x in ingr:
        if is_fresh(x):
            tot = tot + 1

    return tot

def part2(data, verbose=False):
    ranges, _ = data

    def overlapping(a, b):
        a1, a2 = a
        b1, b2 = b
        return (a1 <= b1 and a2 >= b1) or (a1 <= b2 and a2 >= b2) or (a1 >= b1 and a2 <= b2) or (b1 >= a1 and b2 <= a2)

    while True:
        for a, b in combinations(ranges, 2):
            if overlapping(a, b):
                ranges.remove(a)
                ranges.remove(b)
                ranges.add((min(a[0], b[0]), max(a[1], b[1])))
                break
        else:
            break

    return sum(b - a + 1 for (a, b) in ranges)


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
