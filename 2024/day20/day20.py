import time


def parse(data):
    walls = set()
    s = (0, 0)
    e = (0, 0)
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "#":
                walls.add((x, y))
            elif c == "S":
                s = (x, y)
            elif c == "E":
                e = (x, y)
    return walls, s, e


def solve(data, required_gain, max_cheat):
    walls, s, e = data
    p = s

    dist = 0
    path = {p: 0}
    while p != e:
        x, y = p
        dist += 1
        for pp in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if pp not in walls and pp not in path:
                path[pp] = dist
                p = pp
                break

    tot = 0
    for pos, dist in path.items():
        x, y = pos
        for dx in range(x - max_cheat, x + max_cheat + 1):
            for dy in range(y - max_cheat, y + max_cheat + 1):
                cheat_length = abs(x - dx) + abs(y - dy)
                if cheat_length > max_cheat or (dx, dy) not in path:
                    continue

                gain = path[(dx, dy)] - dist - cheat_length
                if gain >= required_gain:
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

run("Part 1 with real input", lambda: solve(lines, required_gain=100, max_cheat=2))
run("Part 2 with real input", lambda: solve(lines, required_gain=100, max_cheat=20))
