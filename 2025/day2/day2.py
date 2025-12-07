import time


def parse(data):
    data = "".join(data)
    data = [r.split("-") for r in data.split(",")]
    return [(a, b) for (a, b) in data]


def part1(data, verbose=False):
    invalid_sum = 0
    for (a,b) in data:
        an = int(a)
        bn = int(b)
        for n in range(an, bn+1):
            s = f"{n}"
            if s[:len(s)//2] == s[len(s)//2:]:
                invalid_sum += n

    return invalid_sum


def part2(data, verbose=False):
    invalid_sum = 0

    for (a,b) in data:
        an = int(a)
        bn = int(b)

        for n in range(an, bn+1):
            s = f"{n}"
            invalids = set()

            for dig in range(0, (len(s) // 2)):
                p = s[0:dig+1]
                for m in range(1, len(s) + 1):
                    comb = p * m
                    if comb == s:
                        if n not in invalids:
                            invalid_sum += n
                            invalids.add(n)

    return invalid_sum


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
