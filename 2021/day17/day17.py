def sim(x, y, dx, dy, target):
    highest = y
    left = min(target[0][0], target[0][1])
    right = max(target[0][0], target[0][1])
    top = max(target[1][0], target[1][1])
    bottom = min(target[1][0], target[1][1])

    while True:
        if x >= left and x <= right and y >= bottom and y <= top:
            return highest

        if y < bottom:
            return None

        x, y = x + dx, y + dy
        if dx > 0:
            dx = dx - 1
        if dx < 0:
            dx = dx + 1
        dy = dy - 1
        highest = max(y, highest)


def solve(target):
    highest = None
    hits = set()

    # Except for min_dy, the other ranges was found
    # by testing until total hit count stabilized.
    min_dy = min(target[1][0], target[1][1])

    for dx in range(-200, 200):
        for dy in range(min_dy, 200):
            r = sim(0, 0, dx, dy, target)
            if r is not None:
                hits.add((dx, dy))
                if highest is None or highest < r:
                    highest = r

    return highest, len(hits)


inp = [(144, 178), (-100, -76)]
example = [(20, 30), (-10, -5)]

inp_result = solve(inp)
example_result = solve(example)

print(f"Part 1 with example data: {example_result[0]}")
print(f"Part 1 with real input: {inp_result[0]}")
print(f"Part 2 with inp data: {example_result[1]}")
print(f"Part 2 with real input: {inp_result[1]}")
