def move_knot(tl, hd):
    if tl[0] < hd[0] - 1:
        tl = (tl[0] + 1, tl[1])
        if tl[1] > hd[1]:
            tl = (tl[0], tl[1] - 1)
        if tl[1] < hd[1]:
            tl = (tl[0], tl[1] + 1)

    if tl[0] > hd[0] + 1:
        tl = (tl[0] - 1, tl[1])
        if tl[1] > hd[1]:
            tl = (tl[0], tl[1] - 1)
        if tl[1] < hd[1]:
            tl = (tl[0], tl[1] + 1)

    if tl[1] < hd[1] - 1:
        tl = (tl[0], tl[1] + 1)
        if tl[0] > hd[0]:
            tl = (tl[0] - 1, tl[1])
        if tl[0] < hd[0]:
            tl = (tl[0] + 1, tl[1])

    if tl[1] > hd[1] + 1:
        tl = (tl[0], tl[1] - 1)
        if tl[0] > hd[0]:
            tl = (tl[0] - 1, tl[1])
        if tl[0] < hd[0]:
            tl = (tl[0] + 1, tl[1])

    return tl


def part1(data, verbose=False):
    visited = set()
    tl = (0, 0)
    hd = (0, 0)
    for line in data:
        d, n = line.split()
        for _ in range(int(n)):
            if d == "R":
                hd = (hd[0] + 1, hd[1])
            elif d == "L":
                hd = (hd[0] - 1, hd[1])
            elif d == "U":
                hd = (hd[0], hd[1] + 1)
            elif d == "D":
                hd = (hd[0], hd[1] - 1)

            tl = move_knot(tl, hd)
            visited.add(tl)

    return len(visited)


def part2(data, verbose=False):
    rope: list[tuple[int, int]] = [(0, 0) for _ in range(10)]
    visited = set()
    for line in data:
        d, n = line.split()
        for _ in range(int(n)):
            hd = rope[0]
            if d == "R":
                hd = (hd[0] + 1, hd[1])
            elif d == "L":
                hd = (hd[0] - 1, hd[1])
            elif d == "U":
                hd = (hd[0], hd[1] + 1)
            elif d == "D":
                hd = (hd[0], hd[1] - 1)
            rope[0] = hd

            for n in range(1, len(rope)):
                rope[n] = move_knot(rope[n], rope[n - 1])

            visited.add(rope[-1])

    return len(visited)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
