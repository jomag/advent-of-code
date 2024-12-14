import math
import re


def parse(data):
    robots = []
    for line in data:
        m = re.match(r"p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)", line)
        if m:
            px, py, vx, vy = map(int, m.groups())
            robots.append((px, py, vx, vy))

    return robots


def print_bathroom(robots, width, height):
    tiles = [[0 for _ in range(width)] for _ in range(height)]
    for r in robots:
        x, y, _, _ = r
        tiles[y][x] += 1
    for row in tiles:
        s = ""
        for tile in row:
            if tile == 0:
                s += "."
            elif tile > 9:
                s += "*"
            else:
                s += str(tile)
        print(s)


def solve(robots, width, height, step_through=False, verbose=False):
    # Set this to true to step through the frames
    # in search of the christmas tree
    search_for_tree = False
    seconds = 100

    def count_quadrants():
        tiles = [[0 for _ in range(width)] for _ in range(height)]
        for r in robots:
            x, y, _, _ = r
            tiles[y][x] += 1

        cx, cy = math.floor(width / 2), math.floor(height / 2)
        q1, q2, q3, q4 = 0, 0, 0, 0

        for y in range(height):
            if y == cy:
                continue
            for x in range(width):
                if x == cx:
                    continue
                if x < cx and y < cy:
                    q1 += tiles[y][x]
                if x > cx and y < cy:
                    q2 += tiles[y][x]
                if x < cx and y > cy:
                    q3 += tiles[y][x]
                if x > cx and y > cy:
                    q4 += tiles[y][x]

        return q1, q2, q3, q4

    for n in range(seconds):
        nr = []
        for px, py, vx, vy in robots:
            px = (px + vx) % width
            py = (py + vy) % height
            nr.append((px, py, vx, vy))
        robots = nr
        if search_for_tree:
            print(f"\nIteration {n+1}")
            print_bathroom(robots, width, height)
            input()

    if verbose:
        print("Final")
        print_bathroom(robots, width, height)

    q1, q2, q3, q4 = count_quadrants()

    return q1 * q2 * q3 * q4


def part2():
    # While thinking about a better solution, such as
    # finding repetition in the positions och finding
    # candidates where many bots were lined up, I
    # rapidly rendered each frame, and glanced
    # the christmas tree at frame 7037.
    #
    # Knowing what the christmas tree looks like, and
    # that it can be found in the first 10.000 seconds,
    # it would be quite simple to find it in any
    # input by automation.
    return 7037


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

print(f"Part 1 with example data: {solve(example, 11,7)}")
print(f"Part 1 with real input: {solve(lines, 101, 103)}")
print(f"Part 2 with real input: {part2()}")
