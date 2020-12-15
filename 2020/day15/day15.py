def part1(inp, turns):
    data = list(inp)

    for i in range(len(data), turns):
        previous = data[i - 1]
        if previous in data[0 : i - 1]:
            rev = data[i - 2 :: -1]
            idx = rev.index(previous) + 1
            data += [idx]
        else:
            data += [0]

    return data[-1]


def part2(inp, turns):
    indices = {inp[i]: i for i in range(len(inp[:-1]))}
    previous = inp[-1]

    for i in range(len(inp), turns):
        try:
            a = i - 1 - indices[previous]
            indices[previous] = i - 1
            previous = a
        except KeyError:
            indices[previous] = i - 1
            previous = 0

    return previous


examples = [
    ((0, 3, 6), 436, 175594),
    ((1, 3, 2), 1, 2578),
    ((2, 1, 3), 10, 3544142),
    ((1, 2, 3), 27, 261214),
    ((2, 3, 1), 78, 6895259),
    ((3, 2, 1), 438, 18),
    ((3, 1, 2), 1836, 362),
]

inp = [1, 20, 11, 6, 12, 0]

for ex in examples + [(inp, 1085)]:
    r = part1(ex[0], 2020)
    if r == ex[1]:
        print(f"Part 1: {ex[0]} => {r}  OK")
    else:
        print(f"Part 1: {ex[0]} => {r}  INVALID")

for ex in examples + [(inp, 1085, 10652)]:
    r = part2(ex[0], 30000000)
    if r == ex[2]:
        print(f"Part 2: {ex[0]} => {r}  OK")
    else:
        print(f"Part 2: {ex[0]} => {r}  INVALID")
