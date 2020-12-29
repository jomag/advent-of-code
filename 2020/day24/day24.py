import sys


def part1(paths):
    black_tiles = set()

    for path in paths:
        x, y = 0, 0
        for d in path:
            if d == "w":
                x = x - 1
            elif d == "e":
                x = x + 1
            elif d == "sw":
                y = y + 1
                if y % 2 == 0:
                    x = x - 1
            elif d == "se":
                y = y + 1
                if y % 2 == 1:
                    x = x + 1
            elif d == "nw":
                y = y - 1
                if y % 2 == 0:
                    x = x - 1
            elif d == "ne":
                y = y - 1
                if y % 2 == 1:
                    x = x + 1
        k = (x, y)
        if k in black_tiles:
            black_tiles.remove(k)
        else:
            black_tiles.add(k)
    return black_tiles


def adjacent(x, y):
    if y % 2 == 0:
        return [
            (x - 1, y),
            (x + 1, y),
            (x, y + 1),
            (x + 1, y + 1),
            (x, y - 1),
            (x + 1, y - 1),
        ]
    else:
        return [
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x - 1, y - 1),
            (x, y - 1),
        ]


def part2(black_tiles):
    t = set()

    for x, y in black_tiles:
        cnt = sum(1 for a in adjacent(x, y) if a in black_tiles)
        if cnt == 1 or cnt == 2:
            t.add((x, y))

        for x2, y2 in adjacent(x, y):
            if (x2, y2) not in black_tiles:
                cnt = sum(1 for a in adjacent(x2, y2) if a in black_tiles)
                if cnt == 2:
                    t.add((x2, y2))

    return t


def print_board(tiles, top, right, bottom, left):
    for y in range(top, bottom):
        if y % 2 == 0:
            line = "  "
        else:
            line = ""
        for x in range(left, right):
            if (x, y) in tiles:
                line += "#   "
            else:
                line += ".   "
        print(line)


paths = []

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    for line in f.readlines():
        line = [c for c in line.strip()]
        path = []
        while len(line) > 0:
            c = line.pop(0)
            if c in ["n", "s"]:
                c = c + line.pop(0)
            path.append(c)
        paths.append(path)

black_tiles = part1(paths)
print(f"Part 1: {len(black_tiles)}")

for n in range(100):
    # print_board(black_tiles, -5, 5, +5, -5)
    # input()
    black_tiles = part2(black_tiles)
    # print(f"Day {n + 1}: {len(black_tiles)}")

print(f"Part 2: {len(black_tiles)}")