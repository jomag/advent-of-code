def part1(data):
    return 1


def part2(data):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
