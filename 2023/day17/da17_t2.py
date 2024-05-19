import math
from typing import Dict, List, Set, Tuple
import heapq


def part1(data: List[str], verbose=False):
    infinite = 1_000_000_000
    width, height = len(data[0]), len(data)

    m: Dict[Tuple[int, int, str, int], int] = {}
    for y, line in enumerate(data):
        for x, heat in enumerate(line):
            for dir in ["n", "w", "s", "e"]:
                for steps in [0, 1, 2]:
                    m[(x, y, dir, steps)] = int(heat)

    distances: Dict[Tuple[int, int, str, int], int] = {}
    previous: Dict[Tuple[int, int, str, int], Tuple[int, int, str, int]] = {}

    q: List[Tuple[int, Tuple[int, int, str, int]]] = []

    start = (0, 0)
    target = (width - 1, height - 1)

    for y in range(height):
        for x in range(width):
            dir = []
            for dir in ["n", "w", "s", "e"]:
                for steps in [0, 1, 2]:
                    t = (x, y, dir, steps)
                    distances[t] = 0 if (x, y) == start else infinite
                    heapq.heappush(q, (distances[t], t))

    finished = set()

    while q:
        print(len(q))
        dist, u = heapq.heappop(q)
        # print(dist, u)

        if u in finished:
            continue
        # if u[0] == target[0] and u[1] == target[1
        # print("FOUND IT! Distance: ", distances[u])
        # break

        x, y, dir, steps = u

        if dir != "s" and (dir != "n" or steps < 2) and y > 0:
            v = (x, y - 1, "n", steps + 1 if dir == "n" else 0)
            if v not in finished:
                alt = dist + m[v]
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
                    heapq.heappush(q, (alt, v))

        if dir != "n" and (dir != "s" or steps < 2) and y < height - 1:
            v = (x, y + 1, "s", steps + 1 if dir == "s" else 0)
            if v not in finished:
                alt = dist + m[v]
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
                    heapq.heappush(q, (alt, v))

        if dir != "e" and (dir != "w" or steps < 2) and x > 0:
            v = (x - 1, y, "w", steps + 1 if dir == "w" else 0)
            if v not in finished:
                alt = dist + m[v]
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
                    heapq.heappush(q, (alt, v))

        if dir != "w" and (dir != "e" or steps < 2) and x < width - 1:
            v = (x + 1, y, "e", steps + 1 if dir == "e" else 0)
            if v not in finished:
                alt = dist + m[v]
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
                    heapq.heappush(q, (alt, v))

    targets = [node for node in m if node[0] == target[0] and node[1] == target[1]]
    best_path: List[Tuple[int, int, str, int]] = []
    lowest_cost = infinite

    for cur in targets:
        path: List[Tuple[int, int, str, int]] = []
        cost = 0
        while cur in previous:
            path.append(previous[cur])
            cost += m[cur]
            cur = previous[cur]
        if cur[0] == start[0] and cur[1] == start[1] and cost < lowest_cost:
            lowest_cost = cost
            best_path = path

    for y in range(height):
        path_opt = [(t[0], t[1]) for t in best_path]
        line = ["#" if (x, y) in path_opt else "." for x in range(width)]
        print(" ".join(line))

    print(list(reversed(best_path)))

    return lowest_cost


def part2(data, verbose=False):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
