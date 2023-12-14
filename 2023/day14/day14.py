def tilt_north_p1(dish):
    w, h = len(dish[0]), len(dish)
    while True:
        moved = False
        for y in range(1, h):
            for x in range(w):
                if dish[y][x] == "O" and dish[y - 1][x] == ".":
                    dish[y][x] = "."
                    dish[y - 1][x] = "O"
                    moved = True
        if not moved:
            break


def tilt_north_p2(dish: tuple):
    w, h = len(dish[0]), len(dish)
    mut = [list(row) for row in dish]

    while True:
        moved = False
        for y in range(1, h):
            for x in range(w):
                if mut[y][x] == "O" and mut[y - 1][x] == ".":
                    mut[y][x] = "."
                    mut[y - 1][x] = "O"
                    moved = True
        if not moved:
            break

    return tuple([tuple(row) for row in mut])


def tilt_south_p2(dish: tuple):
    w, h = len(dish[0]), len(dish)
    mut = [list(row) for row in dish]

    while True:
        moved = False
        for y in range(h - 1):
            for x in range(w):
                if mut[y][x] == "O" and mut[y + 1][x] == ".":
                    mut[y][x] = "."
                    mut[y + 1][x] = "O"
                    moved = True
        if not moved:
            break

    return tuple([tuple(row) for row in mut])


def tilt_west_p2(dish: tuple):
    w, h = len(dish[0]), len(dish)
    mut = [list(row) for row in dish]

    while True:
        moved = False
        for y in range(h):
            for x in range(1, w):
                if mut[y][x] == "O" and mut[y][x - 1] == ".":
                    mut[y][x] = "."
                    mut[y][x - 1] = "O"
                    moved = True
        if not moved:
            break

    return tuple([tuple(row) for row in mut])


def tilt_east_p2(dish: tuple):
    w, h = len(dish[0]), len(dish)
    mut = [list(row) for row in dish]

    while True:
        moved = False
        for y in range(h):
            for x in range(w - 1):
                if mut[y][x] == "O" and mut[y][x + 1] == ".":
                    mut[y][x] = "."
                    mut[y][x + 1] = "O"
                    moved = True
        if not moved:
            break

    return tuple([tuple(row) for row in mut])


def get_load(dish):
    h = len(dish)
    l = 0
    for y, line in enumerate(dish):
        for c in line:
            if c == "O":
                l += h - y
    return l


def print_dish(dish, label="Dish"):
    print(f"{label}:")
    for line in dish:
        print("".join(line))


def part1(data, verbose=False):
    dish = [[c for c in line] for line in data]
    tilt_north_p1(dish)
    return get_load(dish)


def part2(data, verbose=False):
    dish = tuple([tuple([c for c in line]) for line in data])

    visited = {}
    rep = 0

    n = 0
    while dish not in visited:
        visited[dish] = n
        n += 1
        dish = tilt_north_p2(dish)
        dish = tilt_west_p2(dish)
        dish = tilt_south_p2(dish)
        dish = tilt_east_p2(dish)

    rep = n - visited[dish]
    cycles = 1_000_000_000

    for n in range((cycles - (n - rep)) % rep):
        dish = tilt_north_p2(dish)
        dish = tilt_west_p2(dish)
        dish = tilt_south_p2(dish)
        dish = tilt_east_p2(dish)

    return get_load(dish)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
