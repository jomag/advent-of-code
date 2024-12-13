def parse(data):
    machines = []
    ax, ay, bx, by, px, py = [None] * 6
    for line in data:
        if len(line) == 0:
            machines.append((ax, ay, bx, by, px, py))
            ax = None
        else:
            pre, rest = line.split(":")
            xs, ys = rest.split(",")
            x, y = int(xs.strip()[2:]), int(ys.strip()[2:])
            if pre == "Button A":
                ax, ay = x, y
            elif pre == "Button B":
                bx, by = x, y
            elif pre == "Prize":
                px, py = x, y

    if ax:
        machines.append((ax, ay, bx, by, px, py))
    return machines


def part1(data):
    tot = 0

    for machine in data:
        ax, ay, bx, by, px, py = machine
        lowest = None

        for a in range(100):
            for b in range(100):
                if a * ax + b * bx == px and a * ay + b * by == py:
                    cost = a * 3 + b
                    if not lowest or lowest > cost:
                        lowest = cost
        if lowest:
            tot += lowest

    return tot


def part2(data):
    tot = 0

    for machine in data:
        ax, ay, bx, by, px, py = machine
        px, py = px + 10000000000000, py + 10000000000000

        m = ay / ax
        n = by / bx
        x1 = (py - px * n) / (m - n)
        x2 = px - x1

        a = round(x1 / ax)
        b = round(x2 / bx)

        eps = 0.000001
        if abs(a * ax + b * bx - px) < eps and abs(a * ay + b * by - py) < eps:
            tot += a * 3 + b

    return tot


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
