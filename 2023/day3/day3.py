from typing import Dict, List, Tuple


def part1(data: List[str], verbose=False):
    for line in data:
        print(line)
    print("-----------------")

    def at(x, y):
        if y < 0 or y >= len(data):
            return "."
        if x < 0 or x >= len(data[y]):
            return "."
        return data[y][x]

    # Returns true if any neigbhour is a numeric value or a symbol
    def check_neighbours(x, y):
        for xx in [x - 1, x, x + 1]:
            for yy in [y - 1, y, y + 1]:
                if xx != 0 or yy != 0:
                    c = at(xx, yy)
                    if c != "." and not c.isnumeric():
                        return True
        return False

    data2 = []

    for y, line in enumerate(data):
        new_line = ""
        x = 0
        while x < len(line):
            if line[x].isnumeric():
                x1 = x
                x2 = x1
                has_symbol = False
                while x2 < len(line) and line[x2].isnumeric():
                    if check_neighbours(x2, y):
                        has_symbol = True
                    x2 += 1
                if has_symbol:
                    new_line += line[x1:x2]
                else:
                    new_line += "." * (x2 - x1)
                x = x2
            else:
                new_line += "."
                x += 1
        data2.append(new_line)

    for line in data2:
        print(line)

    numbers = []
    for line in data2:
        numbers.extend([int(n) for n in line.split(".") if n != ""])
    print(numbers)
    return sum(numbers)


def part2(data, verbose=False):
    for line in data:
        print(line)
    print("-----------------")

    new_data = []
    for line in data:
        new_line = ""
        for c in line:
            if c.isnumeric() or c == "*":
                new_line += c
            else:
                new_line += "."
        new_data.append(new_line)

    for line in new_data:
        print(line)
    print("-----------------")

    gears: Dict[Tuple[int, int], List[int]] = {}
    for y, line in enumerate(new_data):
        for x, c in enumerate(line):
            if c == "*":
                gears[(x, y)] = []

    def at(x, y):
        if y < 0 or y >= len(data):
            return "."
        if x < 0 or x >= len(data[y]):
            return "."
        return data[y][x]

    def find_neighbour_gear(x, y):
        for xx in [x - 1, x, x + 1]:
            for yy in [y - 1, y, y + 1]:
                if (xx, yy) in gears:
                    return (xx, yy)

    data2 = []

    for y, line in enumerate(data):
        new_line = ""
        x = 0
        while x < len(line):
            if line[x].isnumeric():
                x1 = x
                x2 = x1
                gear = None
                while x2 < len(line) and line[x2].isnumeric():
                    gear = find_neighbour_gear(x2, y) or gear
                    x2 += 1
                if gear:
                    gears[gear].append(int(line[x1:x2]))
                x = x2
            else:
                new_line += "."
                x += 1
        data2.append(new_line)

    print("GEARS:")
    for g in gears:
        print(g, gears[g])

    tot = 0
    for g in gears:
        if len(gears[g]) == 2:
            tot += gears[g][0] * gears[g][1]

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
