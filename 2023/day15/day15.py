def hash(text):
    cv = 0
    for c in text:
        cv += ord(c)
        cv *= 17
        cv = cv % 256
    return cv


def part1(data, verbose=False):
    return sum(hash(s) for s in data[0].split(","))


def part2(data, verbose=False):
    v = "".join(data).split(",")
    print(v)

    instructions = []

    for instr in v:
        try:
            idx = instr.index("=")
            instructions.append((instr[:idx], instr[idx], int(instr[idx + 1 :])))
        except ValueError:
            try:
                idx = instr.index("-")
                instructions.append((instr[:idx], instr[idx]))
            except ValueError:
                raise Exception(f"Invalid instruction: {instr}")

    bx = [[] for _ in range(256)]

    for instr in instructions:
        label = instr[0]
        idx = hash(label)

        if instr[1] == "=":
            value = (label, instr[2])
            for i, b in enumerate(bx[idx]):
                if b[0] == label:
                    bx[idx][i] = value
                    break
            else:
                bx[idx].append(value)

        elif instr[1] == "-":
            for b in bx[idx]:
                if b[0] == label:
                    bx[idx].remove(b)
                    break

        if verbose:
            print(f"\nAfter {instr}")
            for n, b in enumerate(bx):
                if len(b) > 0:
                    print(f"Box {n}: ", b)

    tot = 0
    for i, box in enumerate(bx):
        for j, lens in enumerate(box):
            tot += (i + 1) * (j + 1) * lens[1]

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print("Hash of HASH: ", hash("HASH"))

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
