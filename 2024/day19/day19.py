import time
from functools import cache


def parse(data):
    towels, designs = [], []
    towels = [t.strip() for t in data[0].split(",")]
    assert data[1] == ""
    designs = [d for d in data[2:] if d != ""]
    return towels, designs


def part1(data):
    towels, designs = data

    def build_design(d: str):
        if len(d) == 0:
            return 1
        for t in towels:
            if d.startswith(t):
                if build_design(d[len(t) :]):
                    return 1
        return 0

    return sum(build_design(d) for d in designs)


def part2(data):
    towels, designs = data

    @cache
    def build_design(d: str):
        if len(d) == 0:
            return 1
        tot = 0
        for t in towels:
            if d.startswith(t):
                tot += build_design(d[len(t) :])
        return tot

    return sum(build_design(d) for d in designs)


def run(label, f, data):
    start = time.perf_counter()
    result = f(data)
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

run("Part 1 with example data", part1, example)
run("Part 1 with real input", part1, lines)
run("Part 2 with example data", part2, example)
run("Part 2 with real input", part2, lines)
