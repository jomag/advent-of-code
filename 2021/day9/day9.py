import math


class DepthMap:
    def __init__(self, data):
        self.w = len(data[0])
        self.h = len(data)
        self.m = [[int(d) for d in line] for line in data]

    def at(self, pt):
        if pt[0] < 0 or pt[1] < 0 or pt[0] >= self.w or pt[1] >= self.h:
            return 10
        return self.m[pt[1]][pt[0]]

    def is_low_point(self, x, y):
        depth = self.at((x, y))
        adjacent = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return all([self.at(pt) > depth for pt in adjacent])

    def low_points(self):
        return [
            (x, y)
            for y in range(self.h)
            for x in range(self.w)
            if self.is_low_point(x, y)
        ]

    def basin_size(self, x, y):
        # I could have used a more efficient data structure to keep
        # the checked cells, but this allows easily printing the map.
        checked = [["."] * self.w for _ in range(self.h)]

        def rec(xx, yy, d):
            nonlocal checked

            dd = self.at((xx, yy))
            if dd > 8:
                return

            if checked[yy][xx] == "." and dd > d:
                checked[yy][xx] = str(dd)

            if dd > d:
                rec(xx - 1, yy, dd)
                rec(xx + 1, yy, dd)
                rec(xx, yy - 1, dd)
                rec(xx, yy + 1, dd)

        d = self.at((x, y))
        checked[y][x] = str(d)
        rec(x - 1, y, d)
        rec(x + 1, y, d)
        rec(x, y - 1, d)
        rec(x, y + 1, d)

        return len([b for row in checked for b in row if b != "."])


def part1(data, verbose=False):
    m = DepthMap(data)
    return sum(m.at(pt) + 1 for pt in m.low_points())


def part2(data, verbose=False):
    m = DepthMap(data)
    sizes = [m.basin_size(lp[0], lp[1]) for lp in m.low_points()]
    return math.prod(sorted(sizes)[-3:])


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
