from typing import Optional


def find_shortest_path(start, end, shortest_map, height_map, path=[]):
    if start == end:
        return path

    shortest = None

    sx, sy = start
    width, height = len(height_map[0]), len(height_map)

    for nx, ny in [(sx - 1, sy), (sx + 1, sy), (sx, sy - 1), (sx, sy + 1)]:
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            continue
        if (nx, ny) in path:
            continue
        if height_map[ny][nx] - height_map[sy][sx] > 1:
            continue
        if shortest_map[ny][nx] >= 0 and shortest_map[ny][nx] <= len(path):
            continue

        shortest_map[ny][nx] = len(path)
        p = find_shortest_path(
            (nx, ny), end, shortest_map, height_map, path + [(nx, ny)]
        )
        if p is not None and (shortest is None or len(p) < len(shortest)):
            shortest = p

    return shortest


def solve(data):
    height_map = [[ord(c) - ord("a") for c in line] for line in data]
    width, height = len(height_map[0]), len(height_map)
    shortest_map = [[-1 for x in range(width)] for y in range(height)]

    start, end = (0, 0), (0, 0)
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "S":
                start = x, y
                height_map[y][x] = 0
            if data[y][x] == "E":
                end = x, y
                height_map[y][x] = ord("z") - ord("a")

    p = find_shortest_path(start, end, shortest_map, height_map)
    assert p is not None
    print(f" - Part 1: {len(p)}")

    best = None

    for cy in range(height):
        for cx in range(width):
            if height_map[cy][cx] == 0:
                start = (cx, cy)
                p = find_shortest_path(start, end, shortest_map, height_map)
                if p is not None:
                    if best is None or len(p) < len(best):
                        best = p

    assert best is not None
    print(f" - Part 2: {len(best)}")


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print("Example:")
solve(example)

print("Real data:")
solve(lines)
