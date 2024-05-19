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
    for dir, dist, _ in instr:
        if dir == "R":
            for _ in range(dist):
                x += 1
                if x > max_x:
                    max_x = x
        elif dir == "L":
            for _ in range(dist):
                x -= 1
                if x < min_x:
                    min_x = x
        elif dir == "U":
            for _ in range(dist):
                y -= 1
                if y < min_y:
                    min_y = y
        elif dir == "D":
            for _ in range(dist):
                y += 1
                if y > max_y:
                    max_y = y
        else:
            raise Exception("Invalid direction")
        digs.add((x, y))

    width, height = max_x - min_x, max_y - min_y
    digs = set([(x - min_x, y - min_y) for x, y in digs])

    digs_by_line = []
    for y in range(height):
        line = sorted([d[0] for d in digs if d[1] == y])
        assert len(line) % 2 == 0, f"Was {len(line)}"
        digs_by_line.append(line)

    tot = 0
    for line in digs_by_line:
        for i in range(0, len(line), 2):
            start, end = line[i], line[i + 1]
            tot += end - start + 1

    for line in digs_by_line:
        v = ["." for _ in range(80)]
        for i in range(0, len(line), 2):
            start, end = line[i], line[i + 1]
            for j in range(start, end):
                v[j] = "#"
        print("".join(v))

    return tot


def part2(data, verbose=False):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
