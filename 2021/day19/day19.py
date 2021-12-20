# I will not even attempt to clean up this mess!
# And I seem to have broken the code since I sent in the answer of part 2.
# Puzzle answers are: 313 and 10656, but the current state of this
# solution results in 10678 for part B.


class Scanner:
    beacons: set
    permutations: list[list[tuple]]
    beacons_transformed: list[tuple]

    def __init__(self, idx, beacons):
        self.idx = idx
        self.beacons = set(beacons)
        self.permutations = [[] for n in range(48)]
        self.rel = None

        for x, y, z in beacons:
            directions = [
                (x, y, z),
                (-x, y, z),
                (x, -y, z),
                (-x, -y, z),
                (x, y, -z),
                (-x, y, -z),
                (x, -y, -z),
                (-x, -y, -z),
                (x, z, y),
                (-x, z, y),
                (x, -z, y),
                (-x, -z, y),
                (x, z, -y),
                (-x, z, -y),
                (x, -z, -y),
                (-x, -z, -y),
                (y, x, z),
                (-y, x, z),
                (y, -x, z),
                (-y, -x, z),
                (y, x, -z),
                (-y, x, -z),
                (y, -x, -z),
                (-y, -x, -z),
                (y, z, x),
                (-y, z, x),
                (y, -z, x),
                (-y, -z, x),
                (y, z, -x),
                (-y, z, -x),
                (y, -z, -x),
                (-y, -z, -x),
                (z, x, y),
                (-z, x, y),
                (z, -x, y),
                (-z, -x, y),
                (z, x, -y),
                (-z, x, -y),
                (z, -x, -y),
                (-z, -x, -y),
                (z, y, x),
                (-z, y, x),
                (z, -y, x),
                (-z, -y, x),
                (z, y, -x),
                (-z, y, -x),
                (z, -y, -x),
                (-z, -y, -x),
            ]

            for n in range(len(directions)):
                xx, yy, zz = directions[n]
                self.permutations[n].append((xx, yy, zz))

        assert len(self.permutations) == 48, len(self.permutations)

    def __repr__(self):
        s = f"--- scanner {self.idx} ---\n"
        for b in self.beacons:
            s += f"{b[0]},{b[1]},{b[2]}\n"
        return s


def parse(data):
    lines = [line for line in data if line]
    scanners = []
    beacons = set()
    for line in lines:
        if line[0:3] == "---":
            if beacons:
                scanners.append(Scanner(len(scanners), beacons))
            beacons = set()
        else:
            beacons.add(tuple(int(c) for c in line.split(",")))
    if beacons:
        scanners.append(Scanner(len(scanners), beacons))
    return scanners


offsets = []


def try_merge(s1, s2):
    global offsets

    # First loop:
    # Use all of the beacons in s1 as reference points
    for x1, y1, z1 in s1.beacons:
        # Second loop:
        # Test with all permutations of scanner 2
        for pm in s2.permutations:
            # Third loop:
            # Pick all beacons in the current permutation of s2 and
            # use as reference point for relative distance
            for x2, y2, z2 in pm:
                rx = x2 - x1
                ry = y2 - y1
                rz = z2 - z1

                # We now have:
                # - reference beacon in scanner 1 (x1,y1,z1)
                # - reference beacon in scanner 2 (x2,y2,z2)
                # - relative distance between the two reference beacons (rx,ry,rz)

                # Now we must iterate all beacons in scanner 1 and the current permutation
                # of scanner 2 and see if there are matches
                matches = 0

                for c1 in s1.beacons:
                    rc1 = (c1[0] + rx, c1[1] + ry, c1[2] + rz)
                    if rc1 in pm:
                        matches += 1

                if matches >= 12:
                    print(
                        f"Scanner {s2.idx} can be merged into {s1.idx}! relative: {rx}, {ry}, {rz}. Matches: {matches}"
                    )
                    transformed = set(
                        [(xx - rx, yy - ry, zz - rz) for xx, yy, zz in pm]
                    )
                    offsets.append((rx, ry, rz))
                    print(f"  Len transformed: {len(transformed)}")
                    print(f"  Beacon 0 before {len(s1.beacons)}")

                    print("  Intersection:")
                    print(s1.beacons.intersection(transformed))

                    s1.beacons.update(transformed)
                    print(f"  Total beacons: {len(s1.beacons)}")
                    return True


def part1(data, verbose=False):
    global offsets
    scanners = parse(data)

    scanners[0].beacons_transformed = scanners[0].beacons
    scanners[0].rel = (0, 0, 0)

    known, remaining = scanners[0], scanners[1:]
    finished = False

    prev_remaining = None
    while remaining and not finished:
        if prev_remaining != len(remaining):
            prev_remaining = len(remaining)
            print(f"Remaining: {prev_remaining}")

        still_remaining = []
        finished = True

        for s in remaining:
            if not try_merge(known, s):
                still_remaining.append(s)
            else:
                finished = False

        remaining = still_remaining

    print(remaining)

    def manhattan(o1, o2):
        print(f"{o1} and {o2}")
        return abs(o1[0] - o2[0]) + abs(o1[1] - o2[1]) + abs(o1[2] - o2[2])

    max_distance = 0
    for o in offsets:
        for oo in offsets:
            m = manhattan(o, oo)
            max_distance = max(max_distance, m)
    print("Max distance:", max_distance)

    return len(known.beacons)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Example data: {part1(example, verbose=True)}")
print(f"Puzzle input: {part1(lines)}")
