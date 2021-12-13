def print_paper(dots):
    w = max(dot[0] for dot in dots)
    h = max(dot[1] for dot in dots)
    for y in range(h + 1):
        print("".join("#" if (x, y) in dots else "." for x in range(w + 1)))
    print()


def fold_vertical(y, dots):
    ndots = set()
    for dot in dots:
        if dot[1] > y:
            ny = y - (dot[1] - y)
            ndots.add((dot[0], ny))
        else:
            ndots.add(dot)
    return ndots


def fold_horizontal(x, dots):
    ndots = set()
    for dot in dots:
        if dot[0] > x:
            nx = x - (dot[0] - x)
            ndots.add((nx, dot[1]))
        else:
            ndots.add(dot)
    return ndots


def parse(lines):
    coords = set()
    folds = []
    i = 0
    while i < len(lines) and lines[i] != "":
        x, y = lines[i].split(",")
        coords.add((int(x), int(y)))
        i += 1
    i += 1
    while i < len(lines):
        axis, value = lines[i].split("=")
        folds.append((axis[-1], int(value)))
        i += 1
    return coords, folds


def part1(data, verbose=False):
    coords, folds = parse(data)
    fold = folds[0]
    if fold[0] == "y":
        coords = fold_vertical(fold[1], coords)
    else:
        coords = fold_horizontal(fold[1], coords)

    if verbose:
        print(f"Fold at {fold[0]} = {fold[1]}:")
        print_paper(coords)

    return len(coords)


def part2(data, verbose=False):
    coords, folds = parse(data)

    for fold in folds:
        if fold[0] == "y":
            coords = fold_vertical(fold[1], coords)
        else:
            coords = fold_horizontal(fold[1], coords)

        if verbose:
            print(f"Fold at {fold[0]} = {fold[1]}:")
            print_paper(coords)

    if not verbose:
        print_paper(coords)

    return len(coords)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines,verbose=False)}")
