import time

# Both part 1 and part 2 are solved with brute force.
# For part 1 the map is iterated as is, while for
# part 2 I optimized the algorithm by picking out
# the segments/crossroads first. This improves the
# time for part 2 a lot, but it's still essentially
# the same brute-force algorithm as for part 1.
#
# 5 seconds for part 1 and 42 seconds for part 2.
#
# My first intention was to just use a reversed
# Dijkstra: throw away positions if they've already
# been found with a longer journey. But that can
# fail because reaching the position earlier may
# open up for a longer journey *after* stepping
# on that position. 

def parse(data):
    start = (data[0].index(".") + 1, 1)
    end = (data[-1].index(".") +1, len(data))
    walls = set()
    slopes = {}
    
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "#":
                walls.add((x+1,y+1))
            if c in "<>^v":
                slopes[(x+1,y+1)] = c

    w, h = len(data[0])+2, len(data) + 2
    for x in range(w):
        walls.add((x,0))
        walls.add((x,h-1))

    for y in range(h):
        walls.add((0,y))
        walls.add((w-1,y))

    return start,end,walls,slopes

def print_map(start, end, walls, slopes, paths=[], crossroads={}, path=[]):
    w = max([w[0] for w in walls]) + 1
    h = max([w[1] for w in walls]) + 1
    for y in range(h):
        line = ""
        for x in range(w):
            if (x,y) in path:
                line += "%"
            elif (x,y) in crossroads:
                line += str(len(crossroads[(x, y)]))
            elif (x, y) in walls:
                line += " "
            elif (x,y) in slopes:
                line += slopes[(x,y)]
            elif (x,y) == start:
                line += "S"
            elif (x,y) == end:
                line += "E"
            else:
                for p in paths:
                    if (x,y) in p:
                        line += "O"
                        break
                else:
                    line += "."
        print(line)

def part1(data, verbose=False):
    start,end,walls,slopes = data
    paths = []

    if verbose:
        print_map(start,end,walls,slopes)

    q = [(start[0], start[1], [])]

    while len(q) > 0:
        x, y, path = q.pop()

        path = [*path, (x,y)]

        if (x,y) == end:
            paths.append(set(path))
            continue

        exits = [(x+1,y, "<"), (x-1,y,">"), (x,y+1,"^"), (x, y-1, "v")]
        for exit in exits:
            p = (exit[0], exit[1])
            if p in walls:
                continue
            if p in slopes and slopes[p] == exit[2]:
                continue
            if p not in path:
                q.append((p[0], p[1], path))

    return max([len(p) for p in paths]) - 1


def part2(data):
    start, end, walls, _ = data

    # Queue of tuples: x, y, next-x, next-y
    q = [(start[0], start[1], start[0], start[1]+1)]
    crossroads = {}

    def add_to_crossroads(x1, y1, x2, y2, steps):
        a, b = (x1, y1), (x2, y2)
        if a in crossroads:
            crossroads[a].add((x2, y2, steps))
        else:
            crossroads[a] = set([(x2, y2, steps)])
        if b in crossroads:
            crossroads[b].add((x1, y1, steps))
        else:
            crossroads[b] = set([(x1, y1, steps)])

    visited = set()

    while q:
        ix, iy, x, y = q.pop()
        visited.add((ix, iy))
        steps = 0
        path = set([(ix, iy)])
        local_visited = set([(ix, iy)])

        while True:
            visited.add((x, y))
            local_visited.add((x, y))
            path.add((x,y))

            all_exits = [(x+1,y), (x-1,y), (x,y+1),(x,y-1)]
            possible_exits = [
                p for p in all_exits
                if p not in walls and p not in local_visited
            ]

            if len(possible_exits) == 0:
                if (x, y) == end:
                    add_to_crossroads(ix, iy, x, y, steps+1)
                break
            elif len(possible_exits) == 1:
                x, y = possible_exits[0]
                steps += 1
            else:
                add_to_crossroads(ix, iy, x, y, steps+1)

                possible_exits = [
                    p for p in all_exits
                    if p not in walls and p not in visited
                ]

                for exit in possible_exits:
                    q.append((x, y, exit[0], exit[1]))
                break

    longest = 0
    q = [(start, 0, [start])]
    while q:
        crossing, steps, visited = q.pop()

        if crossing == end:
            if steps > longest:
                longest = steps
            continue

        paths = crossroads[crossing]
        for p in paths:
            endp = (p[0], p[1])
            if endp not in visited:
                v = [*visited, endp]
                q.append((endp, steps + p[2], v))

    return longest

def run(label, f):
    start = time.perf_counter()
    result = f()
    elapsed = time.perf_counter() - start
    if elapsed > 2:
        elapsed = f"{elapsed:.3f}s"
    else:
        elapsed = f"{elapsed*1000:.1f}ms"
    print(f"{label}: {result} ({elapsed})")


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

run("Part 1 with example data", lambda: part1(example, verbose=False))
run("Part 1 with real input", lambda: part1(lines, verbose=False))
run("Part 2 with example data", lambda: part2(example))
run("Part 2 with real input", lambda: part2(lines))
