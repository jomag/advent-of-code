class Forrest:
    def __init__(self, data):
        self.m = [[int(a) for a in line] for line in data]
        self.w = len(self.m[0])
        self.h = len(self.m)

    def visible(self, x, y):
        return (
            self.visible_from_north(x, y)
            or self.visible_from_south(x, y)
            or self.visible_from_west(x, y)
            or self.visible_from_east(x, y)
        )

    def visible_from_north(self, x, y):
        h = self.m[y][x]
        for dy in range(y - 1, -1, -1):
            if self.m[dy][x] >= h:
                return False
        return True

    def visible_from_south(self, x, y):
        h = self.m[y][x]
        for dy in range(y + 1, self.h):
            if self.m[dy][x] >= h:
                return False
        return True

    def visible_from_west(self, x, y):
        h = self.m[y][x]
        for dx in range(x - 1, -1, -1):
            if self.m[y][dx] >= h:
                return False
        return True

    def visible_from_east(self, x, y):
        h = self.m[y][x]
        for dx in range(x + 1, self.w):
            if self.m[y][dx] >= h:
                return False
        return True

    def scenic_score(self, x, y):
        h = self.m[y][x]

        north = 0
        dy = y - 1
        while dy >= 0:
            north += 1
            if self.m[dy][x] >= h:
                break
            dy -= 1

        south = 0
        dy = y + 1
        while dy < self.h:
            south += 1
            if self.m[dy][x] >= h:
                break
            dy += 1

        west = 0
        dx = x - 1
        while dx >= 0:
            west += 1
            if self.m[y][dx] >= h:
                break
            dx -= 1

        east = 0
        dx = x + 1
        while dx < self.w:
            east += 1
            if self.m[y][dx] >= h:
                break
            dx += 1

        return north * south * west * east


def part1(data, verbose=False):
    f = Forrest(data)
    n = 0
    for x in range(f.w):
        for y in range(f.h):
            if f.visible(x, y):
                n += 1

    return n


def part2(data, verbose=False):
    f = Forrest(data)
    highest = 0
    for x in range(f.w):
        for y in range(f.h):
            highest = max(highest, f.scenic_score(x, y))

    return highest


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
