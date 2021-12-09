def parse(data):
    res = []
    for line in data:
        sig, out = line.split("|")
        sig = [i for i in sig.split(" ") if i]
        out = [i for i in out.split(" ") if i]
        res.append((sig, out))
    return res


def part1(data, verbose=False):
    data = parse(data)
    return sum(len([b for b in line[1] if len(b) in [2, 4, 3, 7]]) for line in data)


def xpart2(data, verbose=False):
    data = parse(data)
    tot = 0

    for line in data:
        sig, out = line
        sig = ["".join(s) for s in sig]
        out = ["".join(o) for o in out]

        one = set("".join([x for x in sig if len(x) == 2]))
        four = set("".join([x for x in sig if len(x) == 4]))
        seven = set("".join([x for x in sig if len(x) == 3]))
        eight = set("".join([x for x in sig if len(x) == 7]))
        three = set()
        nine = set()
        two = set()
        five = set()
        six = set()
        zero = set()

        if verbose:
            print(f"ONES: {one}")
            print(f"FOURS: {four}")
            print(f"SEVENS: {seven}")
            print(f"EIGHTS: {eight}")

        # Find THREE
        for m in sig:
            if len(m) == 5:
                if set(m).issuperset(one):
                    three = set(m)

        for m in sig:
            if len(m) == 6:
                if set(m).issuperset(seven):
                    if set(m).issuperset(three):
                        nine = set(m)
                    else:
                        zero = set(m)
                else:
                    six = set(m)

        for m in sig:
            if len(m) == 5:
                if not set(m).issuperset(one):
                    if nine.issuperset(set(m)):
                        five = set(m)
                    else:
                        two = set(m)

        if verbose:
            print(f"THREE: {three}")
            print(f"NINE: {nine}")
            print(f"ZERO: {zero}")
            print(f"SIX: {six}")
            print(f"TWO: {two}")
            print(f"FIVE: {five}")

        digits = [zero, one, two, three, four, five, six, seven, eight, nine]

        s = ""
        for u in out:
            # print(out)
            idx = digits.index(set(u))
            s = f"{s}{idx}"

        tot = tot + int(s)

    return tot


def part2(data, verbose=False):
    data = parse(data)
    tot = 0

    for line in data:
        sig, out = line
        sig = ["".join(s) for s in sig]
        out = ["".join(o) for o in out]

        one = set("".join([x for x in sig if len(x) == 2]))
        four = set("".join([x for x in sig if len(x) == 4]))
        seven = set("".join([x for x in sig if len(x) == 3]))
        eight = set("".join([x for x in sig if len(x) == 7]))
        three = set()
        nine = set()
        two = set()
        five = set()
        six = set()
        zero = set()

        for m in sig:
            if len(m) == 5:
                if set(m).issuperset(one):
                    three = set(m)

        for m in sig:
            if len(m) == 6:
                if set(m).issuperset(seven):
                    if set(m).issuperset(three):
                        nine = set(m)
                    else:
                        zero = set(m)
                else:
                    six = set(m)

        for m in sig:
            if len(m) == 5:
                if not set(m).issuperset(one):
                    if nine.issuperset(set(m)):
                        five = set(m)
                    else:
                        two = set(m)

        digits = [zero, one, two, three, four, five, six, seven, eight, nine]
        s = "".join(str(digits.index(set(u))) for u in out)
        tot = tot + int(s)

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=False)}")
print(f"Part 2 with real input: {part2(lines)}")

assert part1(example) == 26
assert part1(lines) == 375
assert part2(example) == 61229
assert part2(lines) == 1019355
