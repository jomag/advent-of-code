import math


def parse(data):
    instr = list(data[0])
    net = {}
    for line in data[2:]:
        pos, rest = line.split("=")
        pos = pos.strip()
        left, right = rest.replace("(", "").replace(")", "").split(",")
        left, right = left.strip(), right.strip()
        net[pos] = (left, right)
    return instr, net


def part1(data, verbose=False):
    instr, net = parse(data)

    pos = "AAA"
    steps = 0
    while pos != "ZZZ":
        i = instr[steps % len(instr)]
        if i == "L":
            pos = net[pos][0]
        else:
            pos = net[pos][1]
        steps += 1

    return steps


def part2_attempt1_brute_force(data, verbose=False):
    instr, net = parse(data)
    pos = [pos for pos in net if pos[-1] == "A"]

    print(pos)

    steps = 0
    while any(p[-1] != "Z" for p in pos):
        if steps % 1_000_000 == 0:
            print(steps)
        new_pos = []
        for p in pos:
            i = instr[steps % len(instr)]
            if i == "L":
                new_pos.append(net[p][0])
            else:
                new_pos.append(net[p][1])
        steps += 1
        pos = new_pos

    print(pos)
    return steps


def part2(data, verbose=False):
    instr, net = parse(data)
    pos = [pos for pos in net if pos[-1] == "A"]

    initial_steps = []
    rep_steps = []
    second_pos = []

    for p in pos:
        steps = 0
        while p[-1] != "Z":
            i = instr[steps % len(instr)]
            if i == "L":
                p = net[p][0]
            else:
                p = net[p][1]
            steps += 1
        second_pos.append(p)
        initial_steps.append(steps)

    print(pos)
    print(initial_steps)
    print(second_pos)

    for p in second_pos:
        steps = 0
        while True:
            i = instr[steps % len(instr)]
            if i == "L":
                p = net[p][0]
            else:
                p = net[p][1]
            steps += 1
            if p[-1] == "Z":
                break
        rep_steps.append(steps)

    print(rep_steps)

    # Observartion: rep_stpeps and initial_steps are always the same

    lcd = rep_steps[0]
    for s in rep_steps[1:]:
        lcd = (lcd * s) // math.gcd(lcd, s)

    return lcd


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example_p1.txt") as f:
    example_p1 = [ln.strip() for ln in f.readlines()]

with open("example_p2.txt") as f:
    example_p2 = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example_p1, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example_p2, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
