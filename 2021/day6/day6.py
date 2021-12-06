# Part 1 was solved in a naive way. Keeping it, even though the solver
# of part 2 could be used instead, with just another amount of days.
def part1(data, verbose=False):
    def update(fishes):
        nf = []
        for f in fishes:
            if f == 0:
                nf.append(8)
                nf.append(6)
            else:
                nf.append(f - 1)
        return nf

    fishes = [int(d) for d in data[0].split(",")]

    if verbose:
        print(f"Initial state: " + ", ".join(str(i) for i in fishes))

    for day in range(80):
        fishes = update(fishes)
        if verbose:
            print(f"Day {day + 1}: " + ", ".join(str(i) for i in fishes))

    return len(fishes)


def part2(data):
    fishes = [int(d) for d in data[0].split(",")]
    fishes = [fishes.count(n) for n in range(0, 9)]

    for _ in range(256):
        fishes.append(fishes.pop(0))
        fishes[6] += fishes[8]

    return sum(fishes)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
