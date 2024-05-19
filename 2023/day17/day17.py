import sys

sys.setrecursionlimit(150000)


def print_visited(visited, w, h, path=None):
    def sel(x, y):
        if path and (x, y) in path:
            return " @ "
        elif (x, y) in visited:
            return "%03d" % visited[(x, y)]
        else:
            return "..."

    for y in range(h):
        line = [sel(x, y) for x in range(w)]
        print(" ".join(line))


def analyze_path(path, visited, blocks):
    x, y = 0, 0

    heat = blocks[y][x]
    print(f"Start: x, y = {x}, {y}. Block heat: {blocks[y][x]}. Acc: {heat}")

    for i, p in enumerate(path):
        if p == "e":
            x += 1
        elif p == "w":
            x -= 1
        elif p == "n":
            y -= 1
        elif p == "s":
            y += 1

        heat += blocks[y][x]

        print(
            f"Step {i}: direction {p}. x, y = {x}, {y}. Block heat: {blocks[y][x]}. Acc: {heat}"
        )


def part1(data, verbose=False):
    m = [[int(c) for c in line] for line in data]
    visited = {}

    w, h = len(m[0]), len(m)
    attempts = 0

    best_path_so_far = w * 10 + h * 10

    def rec(x, y, heat, dir, travel):
        nonlocal attempts
        nonlocal best_path_so_far
        attempts += 1
        if attempts % 10_000_000 == 0:
            print(f"\nAttempts: {attempts}:")
            print_visited(visited, w, h, None)

        heat += m[y][x]

        if best_path_so_far and heat >= best_path_so_far:
            return None, None

        if (x, y) in visited and visited[(x, y)] < heat:
            return None, None

        visited[(x, y)] = heat

        # At target!
        if x == w - 1 and y == h - 1:
            best_path_so_far = heat
            return heat, dir

        best = None
        best_path = ""

        if (dir != "n" or travel < 2) and dir != "s" and y - 1 >= 0:
            a, p = rec(x, y - 1, heat, "n", (travel + 1 if dir == "n" else 0))
            if a is not None and (best is None or a < best):
                best = a
                best_path = p

        if (dir != "s" or travel < 2) and dir != "n" and y + 1 < h:
            a, p = rec(x, y + 1, heat, "s", (travel + 1 if dir == "s" else 0))
            if a is not None and (best is None or a < best):
                best = a
                best_path = p

        if (dir != "w" or travel < 2) and dir != "e" and x - 1 >= 0:
            a, p = rec(x - 1, y, heat, "w", (travel + 1 if dir == "w" else 0))
            if a is not None and (best is None or a < best):
                best = a
                best_path = p

        if (dir != "e" or travel < 2) and dir != "w" and x + 1 < w:
            a, p = rec(x + 1, y, heat, "e", (travel + 1 if dir == "e" else 0))
            if a is not None and (best is None or a < best):
                best = a
                best_path = p

        if dir is None:
            return best, best_path
        else:
            return best, dir + best_path

    # for a in m:
    # print((" ").join([str(v) for v in a]))

    res, best_path = rec(0, 0, 0, None, 0)
    res = res - m[0][0]

    print("Path: ", " ".join(list(best_path)))
    best_path_blocks = set()

    x, y = 0, 0
    for p in best_path:
        if p == "e":
            x += 1
        elif p == "w":
            x -= 1
        elif p == "n":
            y -= 1
        elif p == "s":
            y += 1
        best_path_blocks.add((x, y))

    print(f"Best result: {res}")
    print_visited(visited, w, h, best_path_blocks)
    print(f"With path:")
    print_visited(visited, w, h, None)

    print("\n\n")
    analyze_path(best_path, visited, m)

    return res


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
