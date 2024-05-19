# 60426: too high
# 47968: too low

# P2 example:   952_408_144_115
#             1_394_588_759_671
#               249 493 379 874

from typing import List, Set, Tuple


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
    vertices: List[Tuple[int, int]] = []
    path_length = 0

    for _, _, color in instr:
        dist = int(color[2:7], 16)
        dir = int(color[7])
        # for dir, dist, color in instr:
        #     dist = int(color[2:7], 16)
        #     dir = int(color[7])
        if dir == "R" or dir == 0:
            x += dist
        elif dir == "L" or dir == 2:
            path.append((x, y, x - dist, y))
            x -= dist
        elif dir == "U" or dir == 3:
            path.append((x, y, x, y - dist))
            y -= dist
        elif dir == "D" or dir == 1:
            path.append((x, y, x, y + dist))
            y += dist
        else:
            raise Exception("Invalid direction")
        vertices.append((x, y))
        path_length += dist

    # vertices = list(reversed(vertices))

    min_x = min(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    vertices = [(v[0] - min_x, v[1] - min_y) for v in vertices]
    width = max(v[0] for v in vertices) + 1
    height = max(v[1] for v in vertices) + 1

    print(f"Width: {width}, Height: {height}")
    # print(len(vertices), vertices)

    a, b = 0, 0
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)
        a += vertices[i][0] * vertices[j][1]
        b += vertices[i][1] * vertices[j][0]

    area = abs(a - b) / 2

    print("Path length: ", path_length)

    return area + path_length // 2 + 1


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
