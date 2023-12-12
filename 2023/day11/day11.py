def solve(expansion_rate, data, verbose=False):
    galaxies = []
    empty_columns = set()
    empty_rows = set()

    for y, line in enumerate(data):
        if all([c == "." for c in line]):
            empty_rows.add(y)

    for x in range(len(data[0])):
        if all([line[x] == "." for line in data]):
            empty_columns.add(x)

    gy = 0
    for y, line in enumerate(data):
        gx = 0
        for x, cell in enumerate(line):
            if cell == "#":
                galaxies.append((gx, gy))
            if x in empty_columns:
                gx += expansion_rate
            else:
                gx += 1
        if y in empty_rows:
            gy += expansion_rate
        else:
            gy += 1

    tot = 0
    for n in range(len(galaxies)):
        a = galaxies[n]
        for m in range(n + 1, len(galaxies)):
            b = galaxies[m]
            tot += abs(b[0] - a[0]) + abs(b[1] - a[1])

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {solve(2, example, verbose=True)}")
print(f"Part 1 with real input: {solve(2, lines)}")
print(f"Part 2 with example data: {solve(1_000_000, example, verbose=True)}")
print(f"Part 2 with real input: {solve(1_000_000, lines)}")
