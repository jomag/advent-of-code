import time
import functools


def parse(data):
    return [tuple(int(b) for b in bank) for bank in data]

def part1(data, verbose=False):
    tot = 0
    for bank in data:
        best = 0
        for i in range(len(bank)):
            for j in range(i+1, len(bank)):
                jolt = bank[i] * 10 + bank[j]
                best = max(jolt, best)
        tot += best

    return tot

def part2(data, verbose=False):
    tot = 0

    for bank in data:
        jolt = 0
        p = 0

        for n in reversed(range(12)):
            slc = bank[p:len(bank)-n]
            best = max(slc)
            p += slc.index(best) + 1
            jolt = jolt * 10 + best

        tot += jolt
    return tot


def brute_force_part2(data, verbose=False):
    """Initial solution, before brain started working"""
    @functools.cache
    def rec(bank, n):
        if n == 0:
            return 0

        best = 0
        for i in reversed(range(len(bank))):
            jolt = bank[i] + rec(bank[:i], n - 1) * 10
            best = max(jolt, best)

        return best

    tot = 0
    for bank in data:
        jolt = rec(bank, 12)
        tot += jolt

    return tot


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
