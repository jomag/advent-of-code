import time


def parse(data):
    schematics = []
    schematic = []
    for line in data:
        if line == "":
            schematics.append(tuple(schematic))
            schematic = []
            continue
        schematic.append(line)
    if len(schematic) > 0:
        schematics.append(schematic)
    return schematics


def part1(data):
    keys = []
    key_heights = []
    locks = []
    lock_heights = []

    for s in data:
        heights = []
        for x in range(len(s[0])):
            y = 0
            while y < len(s):
                if s[y][x] != s[0][x]:
                    break
                y += 1
            heights.append(y-1)

        if all(c == "#" for c in s[0]):
            locks.append(s)
            lock_heights.append(heights)
        else:
            keys.append(s)
            key_heights.append([len(s) - h - 2 for h in heights])

    tot = 0
    for lock in lock_heights:
        for key in key_heights:
            assert len(key) == len(lock)
            if all(lock[x] + key[x] <= 5 for x in range(len(key))):
                tot += 1

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

run("Part 1 with example data", lambda: part1(example))
run("Part 1 with real input", lambda: part1(lines))
