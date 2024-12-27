import time
from itertools import combinations


def parse(data):
    hails = []
    for line in data:
        if "@" in line:
            pos, vel = line.split("@")
            pos = [int(p) for p in pos.split(",")]
            vel = [int(v) for v in vel.split(",")]
            hails.append((pos, vel))

    return hails

def part1(data, verbose=False):
    if len(data) < 20: 
        test_min_x = 7
        test_min_y = 7
        test_max_x = 27
        test_max_y = 27
    else:
        test_min_x = 200000000000000
        test_min_y = 200000000000000
        test_max_x = 400000000000000
        test_max_y = 400000000000000

    tot = 0

    for h1, h2 in combinations(data, 2):
        p1, v1 = h1
        x1, y1, _ = p1
        dx1, dy1, _ = v1

        p2, v2 = h2
        x2, y2, _ = p2
        dx2, dy2, _ = v2

        dy1, dy2 = dy1 / dx1, dy2 / dx2

        if dy1 != dy2:
            x = (x1 * dy1 - x2 * dy2 + y2 - y1) / (dy1 - dy2)
            y = y1 + (x - x1) * dy1

            if verbose:
                print(f"Evaluating {p1}@{v1} and {p2}@{v2}")
                print(f"Collides at {x}, {y}")

            if x >= test_min_x and x <= test_max_x:
                if y >= test_min_y and y <= test_max_y:
                    if (dx1 > 0 and x > x1) or (dx1 < 0 and x < x1):
                        if (dx2 > 0 and x > x2) or (dx2 < 0 and x < x2):
                            if verbose:
                                print("Collides within test!")
                            tot +=1

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
# run("Part 2 with example data", lambda: part2(example, verbose=False))
# run("Part 2 with real input", lambda: part2(lines, verbose=False))
