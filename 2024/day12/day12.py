from collections import deque


def part1(data):
    data = [[".", *[c for c in line], "."] for line in data]
    data = [["."] * len(data[0]), *data, ["."] * len(data[0])]

    def handle_region_at(x, y):
        q = deque([(x, y)])
        c = data[y][x]
        area = 0
        perimeter = 0

        while len(q) > 0:
            xx, yy = q.pop()
            if data[yy][xx] == c:
                data[yy][xx] = c.lower()
                area += 1
                for nx, ny in [(xx - 1, yy), (xx + 1, yy), (xx, yy - 1), (xx, yy + 1)]:
                    if data[ny][nx] in (c, c.lower()):
                        q.append((nx, ny))
                    else:
                        perimeter += 1

        return perimeter * area

    tot = 0
    for y in range(len(data)):
        for x in range(len(data)):
            if data[y][x].isupper():
                tot += handle_region_at(x, y)

    return tot


def part2(data):
    data = [[".", *[c for c in line], "."] for line in data]
    data = [["."] * len(data[0]), *data, ["."] * len(data[0])]

    def handle_region_at(x, y):
        q = deque([(x, y)])
        c = data[y][x]
        area = 0

        north_edges = [set() for _ in range(len(data) - 1)]
        south_edges = [set() for _ in range(len(data) - 1)]
        east_edges = [set() for _ in range(len(data[0]) - 1)]
        west_edges = [set() for _ in range(len(data[0]) - 1)]

        while len(q) > 0:
            xx, yy = q.pop()

            if data[yy][xx] == c:
                alt = (c, c.lower())
                data[yy][xx] = c.lower()
                area += 1

                if data[yy][xx - 1] not in alt:
                    west_edges[xx - 1].add(yy)
                else:
                    q.append((xx - 1, yy))

                if data[yy][xx + 1] not in alt:
                    east_edges[xx].add(yy)
                else:
                    q.append((xx + 1, yy))

                if data[yy - 1][xx] not in alt:
                    north_edges[yy - 1].add(xx)
                else:
                    q.append((xx, yy - 1))

                if data[yy + 1][xx] not in alt:
                    south_edges[yy].add(xx)
                else:
                    q.append((xx, yy + 1))

        edge_count = 0
        for edges in [north_edges, south_edges, west_edges, east_edges]:
            for edge in edges:
                prev = None
                for v in sorted(edge):
                    if v - 1 != prev:
                        edge_count += 1
                    prev = v

        return edge_count * area

    tot = 0
    for y in range(len(data)):
        for x in range(len(data)):
            if data[y][x].isupper():
                tot += handle_region_at(x, y)

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
