from typing import List


class CucumberMap:
    cv: List[List[str]]
    h: int
    w: int

    def __init__(self, data):
        self.cv = [[c for c in line] for line in data]
        self.h = len(self.cv)
        self.w = len(self.cv[0])

    def print(self):
        for line in self.cv:
            print("".join(line))

    def move_east(self):
        buf = [["." for _ in range(self.w)] for _ in range(self.h)]
        n = 0
        for y in range(self.h):
            for x in range(self.w):
                nx = (x + 1) % self.w
                if self.cv[y][x] == ">" and self.cv[y][nx] == ".":
                    buf[y][nx] = ">"
                    n += 1
                elif self.cv[y][x] != ".":
                    buf[y][x] = self.cv[y][x]
        self.cv = buf
        return n

    def move_south(self):
        buf = [["." for _ in range(self.w)] for _ in range(self.h)]
        n = 0
        for y in range(self.h):
            for x in range(self.w):
                ny = (y + 1) % self.h
                if self.cv[y][x] == "v" and self.cv[ny][x] == ".":
                    buf[ny][x] = "v"
                    n += 1
                elif self.cv[y][x] != ".":
                    buf[y][x] = self.cv[y][x]
        self.cv = buf
        return n


def part1(data, verbose=False):
    m = CucumberMap(data)

    if verbose:
        print("Initial state:")
        m.print()

    step = 0
    while True:
        step += 1
        moves = m.move_east()
        moves += m.move_south()

        if verbose:
            print(f"\nAfter {step} step{'' if step == 1 else 's'}")
            m.print()
            input()

        if moves == 0:
            break

    return step


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
