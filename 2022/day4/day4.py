def part1(pairs, verbose=False):
    def contains(a, b):
        return a[0] <= b[0] and a[1] >= b[1]

    n = 0
    for p in pairs:
        if contains(p[0], p[1]) or contains(p[1], p[0]):
            n += 1
    return n


def part2(pairs, verbose=False):
    def overlaps(a, b):
        return a[0] <= b[1] and a[1] >= b[0]

    n = 0
    for p in pairs:
        if overlaps(p[0], p[1]) or overlaps(p[1], p[0]):
            n += 1
    return n


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

pairs_example = []
for ln in example:
    s = ln.split(",")
    s1 = s[0].split("-")
    s2 = s[1].split("-")
    pairs_example.append(((int(s1[0]), int(s1[1])), (int(s2[0]), int(s2[1]))))

pairs = []
for ln in lines:
    s = ln.split(",")
    s1 = s[0].split("-")
    s2 = s[1].split("-")
    pairs.append(((int(s1[0]), int(s1[1])), (int(s2[0]), int(s2[1]))))

print(f"Part 1 with example data: {part1(pairs_example, verbose=True)}")
print(f"Part 1 with real input: {part1(pairs)}")
print(f"Part 2 with example data: {part2(pairs_example, verbose=True)}")
print(f"Part 2 with real input: {part2(pairs)}")
