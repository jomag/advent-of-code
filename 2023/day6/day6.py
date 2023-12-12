def part1(data, verbose=False):
    times = [int(n) for n in data[0].split()[1:]]
    distance = [int(n) for n in data[1].split()[1:]]
    races = [(times[n], distance[n]) for n in range(len(times))]

    tot = 1
    for t, d in races:
        wins = []
        for n in range(t):
            r = (t - n) * n
            if r > d:
                wins.append(n)
        tot = tot * len(wins)
        print(wins)

    return tot


def part2(data, verbose=False):
    t = int(data[0].replace(" ", "").split(":")[1])
    d = int(data[1].replace(" ", "").split(":")[1])

    wins = []
    for n in range(t):
        r = (t - n) * n
        if r > d:
            wins.append(n)

    return len(wins)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
