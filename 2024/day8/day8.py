import itertools
from collections import defaultdict


def solve(data, include_antenna, max_iterations):
    w, h = len(data[0]), len(data)
    antennas = defaultdict(list)
    antinodes = set()

    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c != ".":
                antennas[c].append((x, y))

    for v in antennas.values():
        for a1, a2 in itertools.combinations(v, 2):
            dx, dy = a2[0] - a1[0], a2[1] - a1[1]
            if include_antenna:
                antinodes.add(a1)
                antinodes.add(a2)
            for _ in range(max_iterations):
                a1 = (a1[0] - dx, a1[1] - dy)
                a2 = (a2[0] + dx, a2[1] + dy)
                if a1[0] >= 0 and a1[0] < w and a1[1] >= 0 and a1[1] < h:
                    antinodes.add(a1)
                if a2[0] >= 0 and a2[0] < w and a2[1] >= 0 and a2[1] < h:
                    antinodes.add(a2)

    return len(antinodes)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {solve(example, False,1)}")
print(f"Part 1 with real input: {solve(lines, False,1)}")
print(f"Part 2 with example data: {solve(example,True, 100)}")
print(f"Part 2 with real input: {solve(lines,True, 100)}")
