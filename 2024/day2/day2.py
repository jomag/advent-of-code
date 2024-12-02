def parse(data):
    return [[int(v) for v in line.split()] for line in data]


def part1(data):
    safe = 0
    for line in data:
        p = line[0]
        if p > line[1]:
            for n in range(1, len(line)):
                if p <= line[n] or abs(line[n] - p) > 3:
                    break
                p = line[n]
            else:
                safe += 1
        else:
            for n in range(1, len(line)):
                if p >= line[n] or abs(line[n] - p) > 3:
                    break
                p = line[n]
            else:
                safe += 1
    return safe


def part2(data):
    def test_line(line):
        def is_increasing(line):
            for n in range(len(line) - 1):
                p, pp = line[n], line[n + 1]
                if p >= pp or pp - p > 3:
                    return False
            return True

        def is_increasing_or_decreasing(line):
            return is_increasing(line) or is_increasing(list(reversed(line)))

        if is_increasing_or_decreasing(line):
            return True

        for i in range(len(line)):
            if is_increasing_or_decreasing(line[:i] + line[(i + 1) :]):
                return True

        return False

    return sum([test_line(line) for line in data])


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
