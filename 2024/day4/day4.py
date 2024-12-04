def test_part1_at(data, x, y):
    h, w = len(data), len(data[0])
    word = "XMAS"
    n = 0

    def check(xx, yy, c):
        return xx >= 0 and yy >= 0 and xx < w and yy < h and data[yy][xx] == c

    for i, c in enumerate(word):
        if not check(x + i, y, c):
            break
    else:
        n += 1

    for i, c in enumerate(word):
        if not check(x - i, y, c):
            break
    else:
        n += 1

    for i, c in enumerate(word):
        if not check(x, y + i, c):
            break
    else:
        n += 1

    for i, c in enumerate(word):
        if not check(x, y - i, c):
            break
    else:
        n += 1

    for i, c in enumerate(word):
        if not check(x + i, y + i, c):
            break
    else:
        n += 1

    for i, c in enumerate(word):
        if not check(x - i, y + i, c):
            break
    else:
        n += 1

    for i, c in enumerate(word):
        if not check(x + i, y - i, c):
            break
    else:
        n += 1

    for i, c in enumerate(word):
        if not check(x - i, y - i, c):
            break
    else:
        n += 1

    return n


def part1(data):
    h = len(data)
    w = len(data[0])
    n = 0
    for y in range(h):
        for x in range(w):
            if data[y][x] == "X":
                n += test_part1_at(data, x, y)
    return n


def test_part2_at(data, x, y):
    w1 = "".join([data[y + i][x + i] for i in [-1, 0, 1]])
    w2 = "".join([data[y + i][x - i] for i in [-1, 0, 1]])
    m = ["MAS", "SAM"]
    return w1 in m and w2 in m


def part2(data):
    h = len(data)
    w = len(data[0])
    n = 0

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if test_part2_at(data, x, y):
                n += 1

    return n


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]
with open("example1.txt") as f:
    example1 = [ln.strip() for ln in f.readlines()]
with open("example2.txt") as f:
    example2 = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example1)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example2)}")
print(f"Part 2 with real input: {part2(lines)}")
