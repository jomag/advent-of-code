def print_map(m):
    print("\n".join("".join(str(o if o < 10 else 0) for o in line) for line in m))


def step(m):
    w, h = len(m[0]), len(m)

    total_flash_count = 0
    flash_count = None
    flashed = set()

    for y in range(h):
        for x in range(w):
            m[y][x] += 1

    while flash_count != 0:
        flash_count = 0
        for y in range(h):
            for x in range(w):
                if m[y][x] > 9 and (x, y) not in flashed:
                    flashed.add((x, y))
                    flash_count += 1

                    if y > 0:
                        m[y - 1][x] += 1
                        if x > 0:
                            m[y - 1][x - 1] += 1
                        if x < w - 1:
                            m[y - 1][x + 1] += 1
                    if x > 0:
                        m[y][x - 1] += 1
                    if y < h - 1:
                        m[y + 1][x] += 1
                        if x > 0:
                            m[y + 1][x - 1] += 1
                        if x < w - 1:
                            m[y + 1][x + 1] += 1
                    if x < w - 1:
                        m[y][x + 1] += 1

        total_flash_count += flash_count

    for o in flashed:
        m[o[1]][o[0]] = 0

    return total_flash_count


def part1(data, verbose=False):
    m = [[int(o) for o in line] for line in data]

    if verbose:
        print_map(m)

    total_flash_count = 0

    for i in range(100):
        flash_count = step(m)
        total_flash_count += flash_count
        if verbose:
            print(f"Round {i+1}: {flash_count} flashes")
            print_map(m)

    return total_flash_count


def part2(data, verbose=False):
    m = [[int(o) for o in line] for line in data]
    i = 0

    if verbose:
        print_map(m)

    while sum(o for line in m for o in line) != 0:
        flash_count = step(m)
        if verbose:
            print(f"Round {i+1}: {flash_count} flashes")
            print_map(m)
        i += 1

    return i


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=False)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=False)}")
print(f"Part 2 with real input: {part2(lines)}")
