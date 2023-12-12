def part1(data, verbose=False):
    s = 0
    for line in data:
        digits = [d for d in line if d.isnumeric()]
        value = digits[0] + digits[-1]
        print("value", value)
        num = int(value)
        s = s + num
    return s


def part2(data, verbose=False):
    s = 0
    for line in data:
        oline = line
        line = line.replace("one", "o1e")
        line = line.replace("two", "t2o")
        line = line.replace("three", "t3e")
        line = line.replace("four", "r4r")
        line = line.replace("five", "f5e")
        line = line.replace("six", "s6x")
        line = line.replace("seven", "s7n")
        line = line.replace("eight", "e8t")
        line = line.replace("nine", "n9e")
        # line = line.replace("zero", "0")
        digits = [d for d in line if d.isnumeric()]
        value = digits[0] + digits[-1]
        print("line", oline, "and", line, "value", value)
        num = int(value)
        s = s + num
    return s


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
