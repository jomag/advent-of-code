import functools


def part1(data, verbose=False):
    def check(springs, groups):
        i = 0
        g = []
        while i < len(springs):
            j = 0
            while i + j < len(springs) and springs[i + j] == ".":
                j += 1
            k = 0
            while i + j + k < len(springs) and springs[i + j + k] == "#":
                k += 1
            if k > 0:
                g.append(k)
            i = i + j + k + 1
        if len(g) == len(groups) and all(g[n] == groups[n] for n in range(len(g))):
            return True
        return False

    def find_arrangement_count(springs, groups):
        q = [i for i, c in enumerate(springs) if c == "?"]

        arrangement_count = 0

        for bits in range(2 ** len(q)):
            spr = [c for c in springs]
            for n, idx in enumerate(q):
                if bits & (1 << n) == 0:
                    spr[idx] = "."
                else:
                    spr[idx] = "#"

            spr = "".join(spr)
            if check(spr, groups):
                arrangement_count += 1

        return arrangement_count

    records = []
    for line in data:
        springs, groups = line.split(" ")
        groups = [int(n) for n in groups.split(",")]
        records.append((springs, groups))

    tot = 0
    for r in records:
        tot += find_arrangement_count(r[0], r[1])

    return tot


def part2(data, verbose=False):
    records = []
    for line in data:
        springs, groups = line.split(" ")
        groups = tuple([int(n) for n in groups.split(",")])
        records.append((springs, groups))

    unfolded = []
    for r in records:
        spr = ((r[0] + "?") * 5)[:-1]
        unfolded.append((spr, r[1] * 5))

    @functools.cache
    def rec(spr, groups, indent=""):
        import pudb

        while len(groups) > 0 and len(spr) > 0:
            c = spr[0]

            if c == ".":
                spr = spr[1:]

            elif c == "#":
                for _ in range(groups[0]):
                    if len(spr) == 0 or spr[0] == ".":
                        return 0
                    spr = spr[1:]
                if len(spr) > 0 and spr[0] == "#":
                    return 0
                spr = "." + spr[1:]
                groups = groups[1:]

            else:
                left_spr = "#" + spr[1:]
                left = rec(left_spr, groups, indent + "    ")
                right_spr = "." + spr[1:]
                right = rec(right_spr, groups, indent + "    ")
                return left + right

        if len(groups) == 0 and spr.count("#") == 0:
            return 1
        else:
            return 0

    tot = 0
    for r in unfolded:
        n = rec(r[0], r[1])
        # print(f"{r[0]} {r[1]}: {n} arrangements")
        tot += n

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
