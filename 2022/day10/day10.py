def part1(data, verbose=False):
    cycle = 0
    tot = 0

    def next_cycle():
        nonlocal cycle, tot
        cycle += 1
        if cycle in [20, 60, 100, 140, 180, 220]:
            tot += x * cycle

    x = 1
    for instr in data:
        v = instr.split()
        if v[0] == "noop":
            next_cycle()
        elif v[0] == "addx":
            next_cycle()
            next_cycle()
            x += int(v[1])

    return tot


def part2(data, verbose=False):
    cycle = 0
    row = [" " for _ in range(40)]

    def next_cycle():
        nonlocal cycle, row

        col = cycle % 40
        if abs(col - x) < 2:
            row[col] = "#"

        if col == 39:
            print("".join(row))
            row = [" " for _ in range(40)]

        cycle += 1

    x = 1
    for instr in data:
        v = instr.split()
        if v[0] == "noop":
            next_cycle()
        elif v[0] == "addx":
            next_cycle()
            next_cycle()
            x += int(v[1])


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")

print(f"\nPart 2 with example data:")
part2(example, verbose=True)

print(f"\nPart 2 with real input:")
part2(lines, verbose=True)
