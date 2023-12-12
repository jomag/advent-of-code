import re


def parse(lines):
    p = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    sensors = []
    for line in lines:
        m = p.match(line)
        assert m is not None
        sensors.append(tuple(int(a) for a in m.groups()))
    return sensors


def part1(data, y, verbose=False):
    known = set()

    sensors = parse(data)
    for s in sensors:
        md = abs(s[2] - s[0]) + abs(s[3] - s[1])
        dx = md - abs(s[1] - y)
        min_x = s[0] - dx
        max_x = s[0] + dx

        print(f"Sensor: {s}, md={md}, dx={dx}, range: {min_x} - {max_x}")

        if dx < 0:
            print("Out of range")
            pass
        else:
            for x in range(min_x, max_x + 1):
                known.add(x)

    for s in sensors:
        if s[3] == y and s[2] in known:
            known.remove(s[2])

    print("".join("#" if n in known else "." for n in range(-10, 40)))
    # print(sorted(known))

    return len(known)


class Ranges:
    def __init__(self):
        self.ranges = []

    def add(self, a, b):
        self.ranges.append((a, b))
        ranges = sorted(self.ranges)

        merged = []
        prev = None

        for r in ranges:
            if prev is None:
                prev = r
            else:
                if r[0] <= prev[1]:
                    prev = (prev[0], max(r[1], prev[1]))
                else:
                    merged.append(prev)
                    prev = r

        if prev is not None:
            merged.append(prev)

        self.ranges = merged


def part2(data, lim, verbose=False):
    sensors = parse(data)

    for y in range(3000000, lim + 1):
        if y % 10000 == 0:
            print(f"y={y}...")

        known = Ranges()

        for s in sensors:
            md = abs(s[2] - s[0]) + abs(s[3] - s[1])
            dx = md - abs(s[1] - y)
            min_x = s[0] - dx
            max_x = s[0] + dx

            # print(f"Sensor: {s}, md={md}, dx={dx}, range: {min_x} - {max_x}")

            if dx < 0:
                # print("Out of range")
                pass
            else:
                known.add(max(0, min_x), min(4000000, max_x))

        # for s in sensors:
        #     if s[3] == y and s[2] in known:
        #         known.remove(s[2])

        if len(known.ranges) != 1:
            x = known.ranges[0][1] + 1
            print(f"COORD: {x}, {y}")
            print(known.ranges)
            freq = x * 4000000 + y
            print(f" . freq: {freq}")
            # return freq

    return len(known)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, 10, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines, 2000000)}")
# print(f"Part 2 with example data: {part2(example, 20, verbose=True)}")
print(f"Part 2 with real input: {part2(lines, 4000000)}")

# ranges = Ranges()
# for r in [(10, 30), (40, 60), (25, 35), (35, 40)]:
#     print(f"\nMerge {r}")
#     ranges.add(r[0], r[1])
