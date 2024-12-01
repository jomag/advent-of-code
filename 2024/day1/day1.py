def part1(data):
    grp1 = sorted([int(line.split()[0]) for line in data])
    grp2 = sorted([int(line.split()[1]) for line in data])
    return sum(abs(a - b) for a, b in zip(grp1, grp2))


def part2(data):
    grp1 = [int(line.split()[0]) for line in data]
    grp2 = [int(line.split()[1]) for line in data]
    return sum(a * grp2.count(a) for a in grp1)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
