def parse_stacks(lines):
    stacks = []
    for line in lines:
        if line.strip() == "":
            break
        for n in range(len(line) // 4):
            c = line[n * 4 + 1]
            if c.isalpha():
                while len(stacks) <= n:
                    stacks.append([])
                stacks[n].append(c)
    return stacks


def parse_commands(lines):
    commands = []
    for line in lines:
        parts = line.strip().split(" ")
        if parts[0] == "move":
            commands.append((int(parts[1]), int(parts[3]) - 1, int(parts[5]) - 1))
    return commands


def part1(data):
    stacks = parse_stacks(data)
    commands = parse_commands(data)
    for n, fr, to in commands:
        for _ in range(n):
            c = stacks[fr].pop(0)
            stacks[to].insert(0, c)
    return "".join([st[0] for st in stacks])


def part2(data):
    stacks = parse_stacks(data)
    commands = parse_commands(data)
    for n, fr, to in commands:
        stacks[to] = stacks[fr][:n] + stacks[to]
        stacks[fr] = stacks[fr][n:]
    return "".join([st[0] for st in stacks])


with open("input.txt") as f:
    lines = f.readlines()

with open("example.txt") as f:
    example = f.readlines()

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
