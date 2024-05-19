# 60426: too high
# 47968: too low

# P2 example:   952_408_144_115
#             1_394_588_759_671
#               249 493 379 874

from typing import Dict, List, Set, Tuple


infinite = 1_000_000_000


def part2(data, verbose=False):
    instr: List[Tuple[str, int, str]] = []
    for line in data:
        dir, dist, color = line.split()
        instr.append((dir, int(dist), color))

    min_x, min_y, max_x, max_y = infinite, infinite, -infinite, -infinite
    x, y = 0, 0

    path = []

    # Part 2:
    # for _, _, color in instr:
    #     dist = int(color[2:7], 16)
    #     dir = int(color[7])
    #     if dir == 0:  # "right"
    #         path.append((x, y, x + dist, y))
    #         x += dist
    #     elif dir == 2:  # "left"
    #         path.append((x, y, x - dist, y))
    #         x -= dist
    #     elif dir == 3:  # "up"
    #         path.append((x, y, x, y - dist))
    #         y -= dist
    #     elif dir == 1:  # "down"
    #         path.append((x, y, x, y + dist))
    #         y += dist
    #     else:
    #         raise Exception("Invalid direction")

    # Part 1:

    # Dict where the key is Y, and the value is a list
    # of tuples where first field is X and second is
    # corner type (7FJL).
    # rows: Dict[int, List[Tuple[int, str]]] = {}

    # List of corner tuples: (x, y, direction)
    corners: List[Tuple[int, int, str]] = []

    prev = instr[-1][0]
    print(f"First: {prev}")
    for dir, dist, color in instr:
        if dir == "R":
            if prev == "U":
                corners.append((x, y, "F"))
            if prev == "D":
                corners.append((x, y, "L"))
            x += dist
        elif dir == "L":
            if prev == "U":
                corners.append((x, y, "7"))
            if prev == "D":
                corners.append((x, y, "J"))
            x -= dist
        elif dir == "U":
            if prev == "L":
                corners.append((x, y, "L"))
            if prev == "R":
                corners.append((x, y, "J"))
            y -= dist
        elif dir == "D":
            if prev == "L":
                corners.append((x, y, "F"))
            if prev == "R":
                corners.append((x, y, "7"))
            y += dist
        else:
            raise Exception("Invalid direction")
        prev = dir

    for c in corners:
        print(c)
    print(f"Total: {len(corners)}")
    return 89

    min_x, min_y, max_x, max_y = infinite, infinite, -infinite, -infinite
    for line in path:
        min_x = min(min_x, line[0], line[2])
        max_x = max(max_x, line[0], line[2])
        min_y = min(min_y, line[1], line[3])
        max_y = max(max_y, line[1], line[3])

    path = [(p[0] - min_x, p[1] - min_y, p[2] - min_x, p[3] - min_y) for p in path]
    max_x, max_y = max_x - min_x, max_y - min_y
    min_x, min_y = 0, 0

    width, height = max_x - min_x + 1 + 5, max_y - min_y + 1 + 5
    print(f"Width: {width}, Height: {height}")

    y_events: Set[int] = set()
    for p in path:
        y_events.add(p[1])
        y_events.add(p[3])
        if p[1] == p[3]:
            y_events.add(p[1] + 1)
    y_events_list = sorted(y_events)

    tot = 0

    print(y_events_list)
    y = y_events_list.pop(0)

    while len(y_events_list) > 0:
        print(f"\nEvent at {y}/{height}:\n--------")
        next_y = y_events_list.pop(0)
        intersecting_lines: List[Tuple[int, int, int, int]] = []

        for p in path:
            if p[1] == p[3]:
                if p[1] == y:
                    intersecting_lines.append(p)
            else:
                y1, y2 = min(p[1], p[3]), max(p[1], p[3])
                if y1 < y and y2 > y:
                    intersecting_lines.append(p)
                if y1 < y and y2 == y:
                    intersecting_lines.append(p)
                if y1 == y and y2 > y:
                    intersecting_lines.append(p)

        sorted_intersecting_lines = []
        for line in intersecting_lines:
            if line[0] > line[2]:
                sorted_intersecting_lines.append((line[2], line[3], line[0], line[1]))
            else:
                sorted_intersecting_lines.append(line)
        sorted_intersecting_lines = sorted(
            sorted_intersecting_lines, key=lambda p: p[2]
        )
        sorted_intersecting_lines = sorted(
            sorted_intersecting_lines, key=lambda p: p[0]
        )

        # print(f"lines: {len(sorted_intersecting_lines)}: {sorted_intersecting_lines}")

        digs_on_line = 0
        x = None
        prev = None
        inside = False

        x = sorted_intersecting_lines[0][0]

        for line in sorted_intersecting_lines:
            if line[0] == line[2]:
                y1, y2 = min(line[1], line[2]), max(line[1], line[2])
                if y1 < y and y2 > y:
                    assert line[0] >= x

                    if inside:
                        inside = False
                        digs_on_line += line[0] - x + 1
                        print(f"{line}: (A) x={x} Adding: {line[0] - x + 1}")
                        x = line[0] + 1
                    else:
                        inside = True
                        print(f"{line}: (B) x={x} Entering inner area. Adding 1.")
                        x = line[0] + 1
                        digs_on_line += 1
            else:
                assert line[2] > line[0]
                digs_on_line += line[2] - max(x, line[0])
                print(
                    f"{line}: (C) x={x} Adding {line[2] - x} ({line[0]}, {line[2]}, {x})"
                )
                x = line[2]

        print(f"digs on line {y}: {digs_on_line}. Multiplied by {(next_y - y)}")
        tot += digs_on_line * (next_y - y)
        y = next_y
        input()

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
