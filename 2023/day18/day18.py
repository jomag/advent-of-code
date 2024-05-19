# 60426: too high
# 47968: too low
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
    vert_lines: Set[Tuple[int, int, int]] = set()

    # Tuples of: y, x1, x2
    horz_lines: Set[Tuple[int, int, int]] = set()

    path = []

    for dir, dist, _ in instr:
        if dir == "R":
            horz_lines.add((y, x, x + dist))
            path.append((x, y, x + dist, y))
            x += dist
        elif dir == "L":
            horz_lines.add((y, x - dist, x))
            path.append((x, y, x - dist, y))
            x -= dist
        elif dir == "U":
            vert_lines.add((x, y - dist, y))
            path.append((x, y, x, y - dist))
            y -= dist
        elif dir == "D":
            vert_lines.add((x, y, y + dist))
            path.append((x, y, x, y + dist))
            y += dist
        else:
            raise Exception("Invalid direction")

    min_x, min_y, max_x, max_y = infinite, infinite, -infinite, -infinite
    for line in path:
        min_x = min(min_x, line[0], line[2])
        max_x = max(max_x, line[0], line[2])
        min_y = min(min_y, line[1], line[3])
        max_y = max(max_y, line[1], line[3])
    width, height = max_x - min_x + 1 + 5, max_y - min_y + 1 + 5
    print(f"Width: {width}, Height: {height}")

    path = [(p[0] - min_x, p[1] - min_y, p[2] - min_x, p[3] - min_y) for p in path]
    max_x, max_y = max_x - min_x, max_y - min_y
    min_x, min_y = 0, 0

    field = [[" "] * width for _ in range(height)]

    for n, p in enumerate(path):
        # Vertical line
        if p[0] == p[2]:
            x = p[0]
            y1, y2 = p[1], p[3]
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2):
                field[y][x] = "|"

        # Horizontal line
        elif p[1] == p[3]:
            y = p[1]
            x1, x2 = (p[0], p[2]) if p[0] < p[2] else (p[2], p[0])
            for x in range(x1 + 1, x2):
                field[y][x] = "-"

    def get_direction(line):
        if line[0] == line[2]:
            if line[1] > line[3]:
                return "n"
            else:
                return "s"
        if line[0] < line[2]:
            return "e"
        else:
            return "w"

    for n, p in enumerate(path):
        np = path[(n + 1) % len(path)]
        c = "?"

        d0 = get_direction(p)
        d1 = get_direction(np)

        if d0 in "ns" and d1 in "ns":
            c = "|"
        elif d0 in "ew" and d1 in "ew":
            c = "-"
        elif (d0 == "n" and d1 == "e") or (d0 == "w" and d1 == "s"):
            c = "F"
        elif (d0 == "n" and d1 == "w") or (d0 == "e" and d1 == "s"):
            c = "7"
        elif (d0 == "s" and d1 == "w") or (d0 == "e" and d1 == "n"):
            c = "J"
        elif (d0 == "s" and d1 == "e") or (d0 == "w" and d1 == "n"):
            c = "L"
        else:
            raise Exception(f"Unexpected corner. {d0} -> {d1}")

        field[p[3]][p[2]] = c

    for line in field:
        print("".join(line))

    new_field = []
    for line in field:
        inside = False
        new_line = ""
        for x, c in enumerate(line):
            if c == "L" or c == "J" or c == "|":
                inside = not inside

            if c == " " and inside:
                new_line += "#"
            else:
                new_line += c
        new_field.append(new_line)

    for line in new_field:
        print(line)

    tot = 0
    for line in new_field:
        tot += sum([1 for c in line if c != " "])

    return tot


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
