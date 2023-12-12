def part1(data, verbose=False):
    histories = [[int(n) for n in line.split()] for line in data]
    print(histories)

    total = 0

    for history in histories:
        v = history
        steps = [v]
        while any(n != 0 for n in v):
            v = [v[i + 1] - v[i] for i in range(len(v) - 1)]
            steps.append(v)

        print("Towards zero:")
        for s in steps:
            print(", ".join([str(n) for n in s]))

        # Extrapolate
        steps[-1].append(0)
        for i in reversed(range(len(steps) - 1)):
            steps[i].append(steps[i][-1] + steps[i + 1][-1])

        print("Extrapolated:")
        for s in steps:
            print(", ".join([str(n) for n in s]))

        total += steps[0][-1]

    return total


def part2(data, verbose=False):
    histories = [[int(n) for n in line.split()] for line in data]
    print(histories)

    total = 0

    for history in histories:
        v = history
        steps = [v]
        while any(n != 0 for n in v):
            v = [v[i + 1] - v[i] for i in range(len(v) - 1)]
            steps.append(v)

        print("Towards zero:")
        for s in steps:
            print(", ".join([str(n) for n in s]))

        # Extrapolate
        steps[-1].insert(0, 0)
        for i in reversed(range(len(steps) - 1)):
            steps[i].insert(0, steps[i][0] - steps[i + 1][0])

        print("Extrapolated:")
        for s in steps:
            print(", ".join([str(n) for n in s]))

        total += steps[0][0]

    return total


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
