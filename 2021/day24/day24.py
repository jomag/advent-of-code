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


def run_vm(ops, inp):
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

        if op[0] == "inp":
            var[a] = int(inp[inp_idx])
            inp_idx += 1
        elif op[0] == "add":
            var[a] = value(a) + value(b)
        elif op[0] == "mul":
            var[a] = value(a) * value(b)
        elif op[0] == "div":
            var[a] = value(a) // value(b)
        elif op[0] == "mod":
            var[a] = value(a) % value(b)
        elif op[0] == "eql":
            var[a] = 1 if value(a) == value(b) else 0
        else:
            raise Exception(f"Invalid op: {op}")

    return var


def run_algo(inp):
    a = [1, 1, 1, 1, 1, 26, 1, 26, 26, 1, 26, 26, 26, 26]
    b = [12, 11, 13, 11, 14, -10, 11, -9, -3, 13, -5, -10, -4, -5]
    c = [4, 11, 5, 11, 14, 7, 11, 4, 6, 5, 9, 12, 14, 14]
    w, x, y, z = 0, 0, 0, 0

    # This is the algo, op by op
    # for n in range(14):
    #     w = inp[n]
    #     x *= 0
    #     x += z
    #     x %= 26
    #     z //= a[n]
    #     x += b[n]
    #     x = 1 if x == w else 0
    #     x = 1 if x == 0 else 0
    #     y *= 0
    #     y += 25
    #     y *= x
    #     y += 1
    #     z *= y
    #     y *= 0
    #     y += w
    #     y += c[n]
    #     y *= x
    #     z += y

    # More compact
    # for n in range(14):
    #     x = z % 26
    #     z = z // a[n]
    #     x = x + b[n]
    #     x = 0 if x == inp[n] else 1
    #     y = 25 * x + 1
    #     z = z * y
    #     y = (inp[n] + c[n]) * x
    #     z = z + y

    # Two algos
    # for n in range(14):
    #     if a[n] == 1:
    #         # Algo 1
    #         x = z % 26 + b[n]
    #         if x != inp[n]:
    #             z = 26 * z + inp[n] + c[n]
    #     elif a[n] == 26:
    #         # Algo 2
    #         x = z % 26 + b[n]
    #         z = z // 26
    #         if x != inp[n]:
    #             z = 26 * z + inp[n] + c[n]
    #     else:
    #         raise Exception("Unknown algo")

    # Digit 0
    z = inp[0] + 4

    # Digit 1
    z = 26 * z + inp[1] + 11

    # Digit 2
    z = 26 * z + inp[2] + 5

    # Digit 3
    z = 26 * z + inp[3] + 11

    # Digit 4
    z = 26 * z + inp[4] + 14

    # Digit 0..4
    # z = 2024920 + inp[0] * 456976 + inp[1] * 17576 + inp[2] * 676 + inp[3] * 26 + inp[4]

    # Digit 5
    x = z % 26 - 10
    z = z // 26
    if x != inp[5]:
        z = 26 * z + inp[5] + 7

    # Digit 6
    z = 26 * z + inp[6] + 11

    # Digit 7
    x = z % 26 - 9
    z = z // 26
    if x != inp[6]:
        z = 26 * z + inp[6] + 4

    # Digit 8
    x = z % 26 - 3
    z = z // 26
    if x != inp[7]:
        z = 26 * z + inp[7] + 6

    # Digit 9
    z = 26 * z + inp[6] + 5

    # Digit 10
    x = z % 26 - 5
    z = z // 26
    if x != inp[8]:
        z = 26 * z + inp[8] + 9

    # Digit 11
    x = z % 26 - 10
    z = z // 26
    if x != inp[9]:
        z = 26 * z + inp[9] + 12

    # Digit 12
    x = z % 26 - 4
    z = z // 26
    if x != inp[10]:
        z = 26 * z + inp[10] + 14

    # Digit 13
    x = z % 26 - 5
    z = z // 26
    if x != inp[11]:
        z = 26 * z + inp[11] + 14

    # Same algo as used above:
    w, x, y, z = 0, 0, 0, 0
    for n in range(8, 14):
        if a[n] == 1:
            # Algo 1
            z = 26 * z + inp[n] + c[n]
        elif a[n] == 26:
            # Algo 2
            x = z % 26 + b[n]
            z = z // 26
            if x != inp[n]:
                z = 26 * z + inp[n] + c[n]
        else:
            raise Exception("Unknown algo")

    return {"w": w, "x": x, "y": y, "z": z}


def part1(data, verbose=False):
    ops = parse(data)

    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5]

    print(f"VM:   {run_vm(ops, num)['z']}")
    print(f"Algo: {run_algo(num)['z']}")

    # while True:

    #     for n in range(len(num) - 1, -1, -1):
    #         if num[n] < 9:
    #             num[n] = num[n] + 1
    #             break
    #         else:
    #             num[n] = 1

    #     inp = "".join([str(d) for d in num])
    #     if iter % 10000 == 0:
    #         print(inp)
    #     var = run_vm(ops, inp)
    #     if var["z"] == 0:
    #         print(f"{inp} -> {var}")

    return 1


def part2(data, verbose=False):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
