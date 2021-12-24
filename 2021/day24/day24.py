from typing import Dict


def parse(data):
    a = [line.split(" ") for line in data]
    ops = []
    for aa in a:
        op = [aa[0]]
        for arg in aa[1:]:
            if arg in ["w", "x", "y", "z"]:
                op.append(arg)
            else:
                op.append(int(arg))
        ops.append(op)
    return ops


def run(ops, inp):
    var = {}
    var["x"], var["y"], var["z"], var["w"] = 0, 0, 0, 0
    inp_idx = 0
    a, b = 0, 0

    value = lambda v: int(v) if type(v) is int else int(var[v])

    for op in ops:
        try:
            a = op[1]
            b = op[2]
        except IndexError:
            pass

        match op[0]:
            case "inp":
                var[a] = int(inp[inp_idx])
                inp_idx += 1
            case "add":
                var[a] = value(a) + value(b)
            case "mul":
                var[a] = value(a) * value(b)
            case "div":
                var[a] = value(a) // value(b)
            case "mod":
                var[a] = value(a) % value(b)
            case "eql":
                var[a] = 1 if value(a) == value(b) else 0
            case "_":
                raise Exception(f"Invalid op: {op}")

    return var


def part1(data, verbose=False):
    ops = parse(data)

    num = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    iter = 0

    while True:
        iter += 1

        for n in range(len(num) - 1, -1, -1):
            if num[n] < 9:
                num[n] = num[n] + 1
                break
            else:
                num[n] = 1

        inp = "".join([str(d) for d in num])
        if iter % 10000 == 0:
            print(inp)
        var = run(ops, inp)
        if var["z"] == 0:
            print(f"{inp} -> {var}")

    return 1


def part2(data, verbose=False):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
