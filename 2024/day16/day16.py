import time
from typing import Set, Tuple


def parse(data):
    s, e = None, None
    for y, line in enumerate(data):
        if "E" in line:
            s = (line.find("E"), y)
        if "S" in line:
            s = (line.find("S"), y)
    return data, s, e


def part1(data, verbose=False):
    m, s, _ = data
    x, y = s
    best = {}
    visited = set()

    optimal = None

    q = [(x, y, "E", 0)]

    iter = 0

    while q:
        iter += 1
        if verbose and iter % 1000000 == 0:
            print(f"Iterations: {iter} Queue: {len(q)}")
        x, y, dir, pts = q.pop()
        visited.add((x, y))

        key = (x, y, dir)
        if key in best and best[key] < pts:
            continue
        best[key] = pts

        if m[y][x] == "E":
            if optimal is None or optimal > pts:
                optimal = pts

        def push(x, y, dir, pts):
            key = (x, y, dir)
            if key not in best or best[key] > pts:
                q.append((x, y, dir, pts))

        if dir == "N":
            if m[y - 1][x] != "#":
                push(x, y - 1, dir, pts + 1)
            push(x, y, "W", pts + 1000)
            push(x, y, "E", pts + 1000)

        if dir == "E":
            if m[y][x + 1] == ".":
                push(x + 1, y, dir, pts + 1)
            push(x, y, "N", pts + 1000)
            push(x, y, "S", pts + 1000)

        if dir == "S":
            if m[y + 1][x] == ".":
                push(x, y + 1, dir, pts + 1)
            push(x, y, "E", pts + 1000)
            push(x, y, "W", pts + 1000)

        if dir == "W":
            if m[y][x - 1] == ".":
                push(x - 1, y, dir, pts + 1)
            push(x, y, "N", pts + 1000)
            push(x, y, "S", pts + 1000)

    if verbose:
        for y, line in enumerate(m):
            s = ""
            for x, c in enumerate(line):
                if (x, y) in visited:
                    s += "%"
                else:
                    s += c
            print(s)

    return optimal


def part2(data, verbose=False):
    m, s, _ = data
    x, y = s
    best = {}

    optimal = None
    optimal_paths = []
    optimal_path_visits = set()

    q: Set[Tuple[int, int, str, int, Tuple]] = set()
    q.add((x, y, "E", 0, (s,)))

    iter = 0

    while q:
        iter += 1
        if verbose and iter % 1000000 == 0:
            print(f"Iterations: {iter} Queue: {len(q)}")
        x, y, dir, pts, path = q.pop()

        def push(x, y, dir, pts, path):
            nonlocal optimal
            if m[y][x] == "#":
                return
            if optimal is not None and pts > optimal:
                return
            key = (x, y, dir)
            if key not in best or best[key] >= pts:
                best[key] = pts
                npath = tuple([*path, (x, y)])
                q.add((x, y, dir, pts, npath))

        if m[y][x] == "E":
            if optimal is None or optimal > pts:
                optimal = pts
                optimal_paths = [path]
                optimal_path_visits = set(path)
            elif optimal == pts:
                optimal_paths.append(path)
                for p in path:
                    optimal_path_visits.add(p)
            continue

        if dir == "N":
            push(x, y - 1, dir, pts + 1, path)
            push(x, y, "W", pts + 1000, path)
            push(x, y, "E", pts + 1000, path)

        if dir == "E":
            push(x + 1, y, dir, pts + 1, path)
            push(x, y, "N", pts + 1000, path)
            push(x, y, "S", pts + 1000, path)

        if dir == "S":
            push(x, y + 1, dir, pts + 1, path)
            push(x, y, "E", pts + 1000, path)
            push(x, y, "W", pts + 1000, path)

        if dir == "W":
            push(x - 1, y, dir, pts + 1, path)
            push(x, y, "N", pts + 1000, path)
            push(x, y, "S", pts + 1000, path)

    if verbose:
        for y, line in enumerate(m):
            s = ""
            for x, c in enumerate(line):
                if (x, y) in optimal_path_visits:
                    c = "O"
                s += c
            print(s)

    return len(optimal_path_visits)


def run(label, f, data, verbose=False):
    start = time.perf_counter()
    result = f(data, verbose=verbose)
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

run("Part 1 with example data", part1, example, verbose=False)
run("Part 1 with real input", part1, lines, verbose=False)
run("Part 2 with example data", part2, example, verbose=False)
run("Part 2 with real input", part2, lines, verbose=False)
