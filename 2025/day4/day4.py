import time


def parse(data):
    rolls = set()
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '@':
                rolls.add((x, y))
    return rolls


def part1(rolls, verbose=False):
    n = 0
    for (x,y) in rolls:
        adj = ((x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y+1), (x,y+1), (x+1,y+1))
        if sum(1 for a in adj if a in rolls) < 4:
            n += 1
    return n

def part2(rolls, verbose=False):
    start = len(rolls)
    while True:
        rolls2 = set()
        for (x,y) in rolls:
            adj = ((x-1,y), (x+1,y), (x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y+1), (x,y+1), (x+1,y+1))
            if sum(1 for a in adj if a in rolls) >= 4:
                rolls2.add((x,y))
        if len(rolls) == len(rolls2):
            break
        rolls = rolls2
    return start - len(rolls)


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
