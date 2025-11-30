import time


def parse(data):
    return data


def part1(data, verbose=False):
    return 1


def part2(data, verbose=False):
    return 2


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
# run("Part 1 with real input", lambda: part1(lines, verbose=False))
# run("Part 2 with example data", lambda: part2(example, verbose=False))
# run("Part 2 with real input", lambda: part2(lines, verbose=False))
