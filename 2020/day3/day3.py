from functools import reduce
import operator

with open("input") as f:
    lines = [line.strip() for line in f.readlines()]


def solve(dx: int, dy: int):
    w = len(lines[0])
    cnt = 0
    x = 0

    for line in lines[::dy]:
        if line[x % w] == "#":
            cnt += 1
        x += dx

    return cnt


print(f"Part 1: {solve(3, 1)}")

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
part2 = reduce(operator.mul, [solve(*s) for s in slopes])
print(f"Part 2: {part2}")