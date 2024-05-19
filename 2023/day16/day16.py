def part1(data, verbose=False, start=(0, 0, "e")):
    energized = set()
    visited_rays = set()

    rays = [start]
    w, h = len(data[0]), len(data)

    while True:
        new_rays = []
        for r in rays:
            if r not in visited_rays:
                visited_rays.add(r)
                x, y, dir = r
                if dir == "e":
                    while x < w:
                        energized.add((x, y))
                        if data[y][x] == "\\":
                            new_rays.append((x, y + 1, "s"))
                            break
                        elif data[y][x] == "/":
                            new_rays.append((x, y - 1, "n"))
                            break
                        elif data[y][x] == "|":
                            new_rays.append((x, y + 1, "s"))
                            new_rays.append((x, y - 1, "n"))
                            break
                        x += 1
                elif dir == "w":
                    while x >= 0:
                        energized.add((x, y))
                        if data[y][x] == "\\":
                            new_rays.append((x, y - 1, "n"))
                            break
                        elif data[y][x] == "/":
                            new_rays.append((x, y + 1, "s"))
                            break
                        elif data[y][x] == "|":
                            new_rays.append((x, y + 1, "s"))
                            new_rays.append((x, y - 1, "n"))
                            break
                        x -= 1
                elif dir == "n":
                    while y >= 0:
                        energized.add((x, y))
                        if data[y][x] == "\\":
                            new_rays.append((x - 1, y, "w"))
                            break
                        elif data[y][x] == "/":
                            new_rays.append((x + 1, y, "e"))
                            break
                        elif data[y][x] == "-":
                            new_rays.append((x + 1, y, "e"))
                            new_rays.append((x - 1, y, "w"))
                            break
                        y -= 1
                elif dir == "s":
                    while y < h:
                        energized.add((x, y))
                        if data[y][x] == "\\":
                            new_rays.append((x + 1, y, "e"))
                            break
                        elif data[y][x] == "/":
                            new_rays.append((x - 1, y, "w"))
                            break
                        elif data[y][x] == "-":
                            new_rays.append((x + 1, y, "e"))
                            new_rays.append((x - 1, y, "w"))
                            break
                        y += 1
                else:
                    raise Exception("Invalid direction")

        rays = []
        for r in new_rays:
            if r not in visited_rays:
                rays.append(r)

        if verbose:
            print(rays)

        if verbose:
            for y in range(h):
                print("".join(["#" if (x, y) in energized else "." for x in range(w)]))

        # input()
        if len(rays) == 0:
            break

    if verbose:
        for line in data:
            print(line)
        print()

    return len(energized)


def part2(data, verbose=False):
    w, h = len(data[0]), len(data)

    max_x, max_y, max_energy = 0, 0, 0

    for x in range(w):
        e = part1(data, False, (x, 0, "s"))
        if e > max_energy:
            max_x = x
            max_y = 0
            max_energy = e

    for x in range(w):
        e = part1(data, False, (x, h - 1, "n"))
        if e > max_energy:
            max_x = x
            max_y = h - 1
            max_energy = e

    for y in range(h):
        e = part1(data, False, (0, y, "e"))
        if e > max_energy:
            max_x = 0
            max_y = y
            max_energy = e

    for y in range(h):
        e = part1(data, False, (w - 1, y, "w"))
        if e > max_energy:
            max_x = w - 1
            max_y = y
            max_energy = e

    return max_energy


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
