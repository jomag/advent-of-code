import sys


class Board:
    def __init__(self, filename):
        with open(filename) as f:
            self.m = [[c for c in line.strip()] for line in f.readlines()]

    def adjacent(self, x, y):
        h = len(self.m)
        w = len(self.m[0])
        return [
            self.m[y - 1][x - 1] if x > 0 and y > 0 else None,
            self.m[y - 1][x] if y > 0 else None,
            self.m[y - 1][x + 1] if x + 1 < w and y > 0 else None,
            self.m[y][x - 1] if x > 0 else None,
            self.m[y][x + 1] if x + 1 < w else None,
            self.m[y + 1][x - 1] if x > 0 and y + 1 < h else None,
            self.m[y + 1][x] if y + 1 < h else None,
            self.m[y + 1][x + 1] if x + 1 < w and y + 1 < h else None,
        ]

    def __str__(self):
        return "\n".join(["".join(row) for row in self.m])

    def step_part1(self):
        ch = 0

        def calc(x, y):
            nonlocal ch
            cur = self.m[y][x]
            if cur == ".":
                return "."
            adj = self.adjacent(x, y)

            if cur == "L" and adj.count("#") == 0:
                ch += 1
                return "#"
            elif cur == "#" and adj.count("#") > 3:
                ch += 1
                return "L"
            else:
                return cur

        h = len(self.m)
        w = len(self.m[0])
        self.m = [[calc(x, y) for x in range(w)] for y in range(h)]
        return ch

    def look(self, nx, ny, dx, dy, dist=None):
        h, w = len(self.m), len(self.m[0])
        nx, ny = nx + dx, ny + dy
        while dist != 0 and nx >= 0 and nx < w and ny >= 0 and ny < h:
            if self.m[ny][nx] != ".":
                return self.m[ny][nx]
            nx, ny = nx + dx, ny + dy
            if dist is not None:
                dist -= 1

    def step_part2(self):
        h = len(self.m)
        w = len(self.m[0])
        ch = 0

        def adjacent(x, y):
            return [
                self.look(x, y, -1, -1),
                self.look(x, y, 0, -1),
                self.look(x, y, 1, -1),
                self.look(x, y, -1, 0),
                self.look(x, y, 1, 0),
                self.look(x, y, -1, 1),
                self.look(x, y, 0, 1),
                self.look(x, y, 1, 1),
            ]

        def calc(x, y):
            nonlocal ch
            cur = self.m[y][x]
            if cur == ".":
                return "."
            adj = adjacent(x, y)

            if cur == "L" and adj.count("#") == 0:
                ch += 1
                return "#"
            elif cur == "#" and adj.count("#") > 4:
                ch += 1
                return "L"
            else:
                return cur

        h = len(self.m)
        w = len(self.m[0])
        self.m = [[calc(x, y) for x in range(w)] for y in range(h)]
        return ch

    def seated_count(self):
        return sum(row.count("#") for row in self.m)


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
b = Board(filename)
r = 1
while b.step_part1() > 0:
    print(f"\nRound {r}:")
    print(b)
    r += 1

print(f"Seated after {r} rounds: {b.seated_count()}")

b = Board(filename)
r = 1
while b.step_part2() > 0:
    print(f"\nRound {r}:")
    print(b)
    r += 1

print(f"Seated after {r} rounds: {b.seated_count()}")
