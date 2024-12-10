def parse(data):
    m = [[-1 if c == "." else int(c) for c in line] for line in data]
    m = [[-1] + line + [-1] for line in m]
    m = [[-1] * len(m[0])] + m + ([[-1] * len(m[-1])])
    sp = [(x, y) for y, line in enumerate(m) for x, c in enumerate(line) if c == 0]
    return m, sp


def part1(data):
    m, sp = data

    def reachable_from(x, y):
        tops = set()

        def hike(x, y):
            lvl = m[y][x]
            if lvl == 9:
                tops.add((x, y))
                return
            for xx, yy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if m[yy][xx] == lvl + 1:
                    hike(xx, yy)

        hike(x, y)
        return len(tops)

    return sum(reachable_from(x, y) for x, y in sp)


def part2(data):
    m, sp = data

    def trails_from(x, y):
        trails = set()

        def hike(x, y, path):
            lvl = m[y][x]
            if lvl == 9:
                trails.add(path)
                return
            for xx, yy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if m[yy][xx] == lvl + 1:
                    hike(xx, yy, path + ((xx, yy)))

        hike(x, y, tuple())
        return len(trails)

    return sum(trails_from(x, y) for x, y in sp)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
