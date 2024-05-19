# 60426: too high

from typing import List, Set, Tuple


infinite = 1_000_000_000


def part1(data, verbose=False):
    instr: List[Tuple[str, int, str]] = []
    for line in data:
        dir, dist, color = line.split()
        instr.append((dir, int(dist), color))

    digs: Set[Tuple[int, int]] = set()
    min_x, min_y, max_x, max_y = infinite, infinite, -infinite, -infinite
    x, y = 0, 0

    # Tuples of: x, y1, y2
    vertical_lines: Set[Tuple[int, int, int]] = set()

    for dir, dist, _ in instr:
        if dir == "R":
            x += dist
        elif dir == "L":
            x -= dist
        elif dir == "U":
            vertical_lines.add((x, y - dist, y))
            y -= dist
        elif dir == "D":
            vertical_lines.add((x, y, y + dist))
            y += dist
        else:
            raise Exception("Invalid direction")

    min_x = min([l[0] for l in vertical_lines])
    max_x = max([l[0] for l in vertical_lines])
    min_y = min([l[1] for l in vertical_lines])
    max_y = max([l[2] for l in vertical_lines])
    width, height = max_x - min_x + 1, max_y - min_y + 1
    print(f"Width: {width}, Height: {height}")

    return 0


def part2(data, verbose=False):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
