def part1(walls, verbose=False):
    pour_at = (500, 0)
    resting = set()

    def find_wall_below(x, y):
        for w in walls:
            if w[0] <= x and x <= w[0] + w[2] and y <= w[1]:
                return w
        return None

    def is_blocked(x, y):
        for w in walls:
            if w[0] <= x and x <= w[0] + w[2] and w[1] <= y and y <= w[1] + w[3]:
                return True
        return (x, y) in resting

    def simulate_drop(x, y):
        w = find_wall_below(x, y)
        if w is None:
            print("Fell into the abyss!")
            return False
        dy = w[1] - 1
        while is_blocked(x, dy):
            dy -= 1
        if not is_blocked(x - 1, dy + 1):
            return simulate_drop(x - 1, dy + 1)
        elif not is_blocked(x + 1, dy + 1):
            return simulate_drop(x + 1, dy + 1)
        resting.add((x, dy))
        return True

    while simulate_drop(pour_at[0], pour_at[1]):
        if verbose:
            print(resting)

    return len(resting)


def part2(walls, verbose=False):
    pour_at = (500, 0)
    resting = {}
    highest = None

    lowest = 0
    for w in walls:
        lowest = max(lowest, w[1], w[1] + w[3])

    print(f"Lowest wall at {lowest}")
    walls.append((-2_000, lowest + 2, +4_000, 0))

    def find_wall_below(x, y):
        for w in walls:
            if w[0] <= x and x <= w[0] + w[2] and y <= w[1]:
                return w
        return None

    def is_blocked_by_wall(x, y):
        for w in walls:
            if w[0] <= x and x <= w[0] + w[2] and w[1] <= y and y <= w[1] + w[3]:
                return True
        return False

    def is_blocked_by_sand(x, y):
        return x in resting and y in resting[x]

    def is_blocked(x, y):
        return is_blocked_by_wall(x, y) or is_blocked_by_sand(x, y)

    def print_playfield():
        def xy_to_char(x, y):
            if is_blocked_by_wall(x, y):
                return "#"
            if is_blocked_by_sand(x, y):
                return "o"
            return "."

        # min_x = min(w[0] for w in walls if w[0] > -2000) - 10
        # max_x = max(w[0] + w[1] for w in walls if w[0] > -2000) + 10
        min_x = 500 - 200
        max_x = 500 + 100
        min_y = 0
        max_y = lowest + 5

        for y in range(min_y, max_y):
            print("".join(xy_to_char(x, y) for x in range(min_x, max_x)))

    def simulate_drop(x, y):
        nonlocal highest
        w = find_wall_below(x, y)

        if w is None:
            print("Fell into the abyss!")
            return False

        dy = w[1] - 1
        while is_blocked(x, dy):
            dy -= 1

        if dy < 0:
            print("Flooded!")
            return False

        if not is_blocked(x - 1, dy + 1):
            return simulate_drop(x - 1, dy + 1)
        elif not is_blocked(x + 1, dy + 1):
            return simulate_drop(x + 1, dy + 1)

        if highest is None or dy < highest:
            highest = dy
            print(f"At: {dy}")

        if x in resting:
            resting[x].add(dy)
        else:
            resting[x] = set([dy])
        return True

    drops = 0
    while simulate_drop(pour_at[0], pour_at[1]):
        drops += 1
        if drops == 1 or drops % 1_000 == 0:
            print_playfield()
            print(f"Drops: {drops} ({len(resting)})")
        if verbose:
            print(resting)

    print(resting)
    print_playfield()
    return sum(len(resting[rx]) for rx in resting)


def parse(lines):
    walls = []
    for line in lines:
        a = [c.split(",") for c in line.split(" -> ")]
        seg = [(int(b[0]), int(b[1])) for b in a]
        for i in range(len(seg) - 1):
            x1, y1, x2, y2 = seg[i][0], seg[i][1], seg[i + 1][0], seg[i + 1][1]
            if (y1 == y2 and x1 > x2) or (x1 == x2 and y1 > y2):
                x1, y1, x2, y2 = x2, y2, x1, y1
            walls.append((x1, y1, x2 - x1, y2 - y1))
    print(walls)
    return sorted(walls, key=lambda c: c[1])


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(parse(example), verbose=True)}")
print(f"Part 1 with real input: {part1(parse(lines))}")
# print(f"Part 2 with example data: {part2(parse(example), verbose=True)}")
# print(f"Part 2 with real input: {part2(parse(lines))}")
