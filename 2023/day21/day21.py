def part1(data, steps, verbose=False):
    m = [["#"] * (len(data[0]) + 2)]
    for line in data:
        m.append(["#"] + [c for c in line] + ["#"])
    m.append(["#"] * (len(data[0]) + 2))

    width, height = len(m[0]), len(m)

    for n in range(steps + 1):
        if verbose:
            print(f"\nStep {n}:")
        p = 0
        for r in m:
            if verbose:
                print("".join(r))
            p += r.count("O")
        if verbose:
            print(f"Possibilities: {p}")
            input()

        m2 = []
        for line in m:
            m2.append([("." if c in "OS" else c) for c in line])

        for y in range(height):
            for x in range(width):
                if m[y][x] in "OS":
                    for xx, yy in [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]:
                        if m2[yy][xx] == ".":
                            m2[yy][xx] = "O"

        m = m2

    return p


def part2(data, verbose=False):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, 6, verbose=True)}")
print(f"Part 1 with real input: {part1(lines,64)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
