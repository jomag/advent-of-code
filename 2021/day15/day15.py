from typing import List, Union


def parse(data):
    m = [[int(c) for c in line] for line in data]
    w = len(m[0])
    h = len(m)
    return m, w, h


def part1(data, verbose=False):
    # Naive recursive solution that tests all paths recursively, with
    # some early returns as a minor optmiziation. This takes a long time
    # to run (more than a minute), but works for part 1. Part 2 required
    # a better approach.
    m, w, h = parse(data)
    min_risk_map = [[None for _ in range(w)] for _ in range(h)]

    min_risk = None
    min_risk_path = None

    def rec(x, y, risk, path):
        nonlocal min_risk
        nonlocal min_risk_path

        if y > 0 or x > 0:
            risk = risk + m[y][x]
        path = [p for p in path] + [(x, y)]

        if min_risk_map[y][x] is None or min_risk_map[y][x] > risk:
            min_risk_map[y][x] = risk
        else:
            return

        if not min_risk or risk < min_risk:
            if x == w - 1 and y == h - 1:
                min_risk = risk
                min_risk_path = path
            else:
                if x + 1 < w:
                    rec(x + 1, y, risk, path)
                if y + 1 < h:
                    rec(x, y + 1, risk, path)
                if x > 0:
                    rec(x - 1, y, risk, path)
                if y > 0:
                    rec(x, y - 1, risk, path)

    rec(0, 0, 0, [])

    if verbose and min_risk_path is not None:
        for y in range(h):
            print(
                "".join(
                    ["*" if (x, y) in min_risk_path else str(m[y][x]) for x in range(w)]
                )
            )

    return min_risk


def part2(data):
    mo, w, h = parse(data)
    scale = 5

    m = [[0 for _ in range(w * scale)] for _ in range(h * scale)]
    for ry in range(scale):
        for y in range(h):
            for rx in range(scale):
                for x in range(w):
                    n = (mo[y][x] - 1 + ry + rx) % 9 + 1
                    m[ry * h + y][rx * w + x] = n

    w = w * scale
    h = h * scale

    min_risk_map: List[List[Union[int, None]]] = [
        [None for _ in range(w)] for _ in range(h)
    ]

    revisits = set([(x, y) for y in range(h) for x in range(w)])
    min_risk_map[0][0] = 0

    while len(revisits) > 0:
        next_revisits = set()

        for x, y in revisits:

            neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            neighbours = [
                (xx, yy)
                for xx, yy in neighbours
                if xx >= 0 and xx < w and yy >= 0 and yy < h
            ]

            neighbour_risks = [min_risk_map[yy][xx] for xx, yy in neighbours]
            neighbour_risks = [r for r in neighbour_risks if r is not None]

            if neighbour_risks:
                current_risk = min_risk_map[y][x]
                new_risk = min(neighbour_risks) + m[y][x]
                if current_risk is None or current_risk > new_risk:
                    min_risk_map[y][x] = new_risk
                    next_revisits.update(neighbours)

        revisits = next_revisits

    return min_risk_map[h - 1][w - 1]


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
