def parse(data):
    w, h = len(data[0]), len(data)
    obstacles = set()
    guard = None
    for y, line in enumerate(data):
        for x, val in enumerate(line):
            if val == "#":
                obstacles.add((x, y))
            if val in ["^", "<", ">", "v"]:
                guard = (x, y, val)
    return (w, h, obstacles, guard)


def print_map(w, h, obs, g, visited=None, loop_obs=None):
    for y in range(h):
        line = ""
        for x in range(w):
            if loop_obs and (x, y) in loop_obs:
                line += "O"
            elif (x, y) in obs:
                line += "#"
            elif g[0] == x and g[1] == y:
                line += g[2]
            elif visited and (x, y) in visited:
                line += "x"
            else:
                line += "."
        print(line)


def part1(data, verbose=False):
    w, h, obs, g = data
    x, y, dir = g
    visited = set()

    if verbose:
        print("Before:")
        print_map(w, h, obs, g)

    while x >= 0 and y >= 0 and x < w and y < h:
        visited.add((x, y))
        if dir == "^":
            if (x, y - 1) in obs:
                dir = ">"
            else:
                y = y - 1
        elif dir == ">":
            if (x + 1, y) in obs:
                dir = "v"
            else:
                x = x + 1
        elif dir == "v":
            if (x, y + 1) in obs:
                dir = "<"
            else:
                y = y + 1
        elif dir == "<":
            if (x - 1, y) in obs:
                dir = "^"
            else:
                x = x - 1

    if verbose:
        print("\nAfter:")
        print_map(w, h, obs, g, visited)

    return len(visited)


def part2(data, verbose=False):
    w, h, obs, g = data

    def detect_loop(ox, oy):
        x, y, dir = g
        visited = set()

        while x >= 0 and y >= 0 and x < w and y < h:
            if (x, y, dir) in visited:
                return True
            visited.add((x, y, dir))

            if dir == "^":
                if (x, y - 1) in obs or (x, y - 1) == (ox, oy):
                    dir = ">"
                else:
                    y = y - 1
            elif dir == ">":
                if (x + 1, y) in obs or (x + 1, y) == (ox, oy):
                    dir = "v"
                else:
                    x = x + 1
            elif dir == "v":
                if (x, y + 1) in obs or (x, y + 1) == (ox, oy):
                    dir = "<"
                else:
                    y = y + 1
            elif dir == "<":
                if (x - 1, y) in obs or (x - 1, y) == (ox, oy):
                    dir = "^"
                else:
                    x = x - 1
        return False

    loop_obs = set()
    for y in range(h):
        for x in range(w):
            if detect_loop(x, y):
                loop_obs.add((x, y))

    if verbose:
        print("\nAfter:")
        print_map(w, h, obs, g, None, loop_obs)

    return len(loop_obs)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
