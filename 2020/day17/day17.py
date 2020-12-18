import sys


def part1(b):
    """
    For each round, the board is expanded by 1 in each direction: 3x3x3 -> 5x5x5.
    All coordinates reference the *new* board size, if not stated otherwise.
    """

    def at(x, y, z):
        if x <= 0 or y <= 0 or z <= 0:
            return "."
        if x >= width - 1 or y >= height - 1 or z >= depth - 1:
            return "."
        return b[z - 1][y - 1][x - 1]

    def find_adjacent(x, y, z):
        return [
            at(dx, dy, dz)
            for dz in range(z - 1, z + 2)
            for dy in range(y - 1, y + 2)
            for dx in range(x - 1, x + 2)
            if dx != x or dy != y or dz != z
        ]

    width = len(b[0][0]) + 2
    height = len(b[0]) + 2
    depth = len(b) + 2

    bn = [[["."] * width for _ in range(height)] for _ in range(depth)]

    for z in range(depth + 2):
        for y in range(height + 2):
            for x in range(width + 2):
                adjacent = find_adjacent(x, y, z)
                n = sum(1 for a in adjacent if a == "#")
                if at(x, y, z) == "#":
                    if n == 2 or n == 3:
                        bn[z][y][x] = "#"
                else:
                    if n == 3:
                        bn[z][y][x] = "#"

    return bn


def part2(b):
    """
    For each round, the board is expanded by 1 in each direction: 3x3x3 -> 5x5x5.
    All coordinates reference the *new* board size, if not stated otherwise.
    """

    def at(x, y, z, w):
        if x <= 0 or y <= 0 or z <= 0 or w <= 0:
            return "."
        if x >= width - 1 or y >= height - 1 or z >= depth - 1 or w >= zork - 1:
            return "."
        return b[w - 1][z - 1][y - 1][x - 1]

    def find_adjacent(x, y, z, w):
        return [
            at(dx, dy, dz, dw)
            for dw in range(w - 1, w + 2)
            for dz in range(z - 1, z + 2)
            for dy in range(y - 1, y + 2)
            for dx in range(x - 1, x + 2)
            if dx != x or dy != y or dz != z or dw != w
        ]

    width = len(b[0][0][0]) + 2
    height = len(b[0][0]) + 2
    depth = len(b[0]) + 2
    zork = len(b) + 2

    bn = [
        [[["."] * width for _ in range(height)] for _ in range(depth)]
        for _ in range(zork)
    ]

    for w in range(zork + 2):
        for z in range(depth + 2):
            for y in range(height + 2):
                for x in range(width + 2):
                    adjacent = find_adjacent(x, y, z, w)
                    n = sum(1 for a in adjacent if a == "#")
                    if at(x, y, z, w) == "#":
                        if n == 2 or n == 3:
                            bn[w][z][y][x] = "#"
                    else:
                        if n == 3:
                            bn[w][z][y][x] = "#"

    return bn


def print_board3d(b):
    for z in range(len(b)):
        print(f"Z={z}:")
        for y in range(len(b[0][0])):
            print("".join(b[z][y]))


def print_board4d(b):
    for w in range(len(b)):
        for z in range(len(b[0])):
            print(f"W={w} Z={z}:")
            for y in range(len(b[0][0][0])):
                print("".join(b[w][z][y]))


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]

width = len(lines[0])
height = len(lines)
board3d = [[["."] * width for _ in range(height)]]
board4d = [[[["."] * width for _ in range(height)]]]

for x in range(width):
    for y in range(height):
        board3d[0][y][x] = lines[y][x]
        board4d[0][0][y][x] = lines[y][x]

for n in range(6):
    board3d = part1(board3d)

part1 = sum(1 for dim in board3d for row in dim for cell in row if cell == "#")
print(f"Part 1: {part1}")

for n in range(6):
    board4d = part2(board4d)

part2 = sum(
    1 for zork in board4d for dim in zork for row in dim for cell in row if cell == "#"
)
print(f"Part 2: {part2}")
