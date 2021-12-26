# The idea for this one is that there are two types of algorithms
# in the input program, and every digit is processed by either
# algorithm 1 or algorithm 2:
#
# - Algorithm 1 multiplies `z` by 26
# - Algorithm 2 divides `z` by 26
#
# There's more happening than that: there's one value that varies
# with each invocation of algo 1, and 2 values for algo 2.
# But to allow `z` to end up zero, algo 2 must always negate
# algo 1. But the algorihms are a bit random. If we consider
# the result as a stack (multiply by 26 is "push", divide by
# 26 is "pop"), then my input had the following push and pops:
#
# Digit 0: push
# Digit 1: push
# Digit 2: push
# Digit 3: push
# Digit 4: push
# Digit 5: pop digit 4
# Digit 6: push
# Digit 7: pop digit 6
# Digit 8: pop digit 3
# Digit 9: push
# Digit 10: pop digit 9
# Digit 11: pop digit 2
# Digit 12: pop digit 1
# Digit 13: pop digit 0
#
# With these rules in place, I only had to find a combination
# of input values for the push and pop pairs that resulted in zero.

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


def run_vm(ops, inp, stop_at=None):
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
            if stop_at == inp_idx:
                return var
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


def algo(w, z, a, b, c):
    if a == 1:
        z = 26 * z + w + b
    else:
        x = z % 26 + b
        z = z // 26
        if x != w:
            z = 26 * z + w + c
    return z


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

    # # Digit 1
    z = 26 * z + inp[1] + 11

    # # Digit 2
    z = 26 * z + inp[2] + 5

    # # Digit 3
    z = 26 * z + inp[3] + 11

    # # Digit 4
    z = 26 * z + inp[4] + 14

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
    if x != inp[7]:
        z = 26 * z + inp[7] + 4

    # Digit 8
    x = z % 26 - 3
    z = z // 26
    if x != inp[8]:
        z = 26 * z + inp[8] + 6

    # Digit 9
    z = 26 * z + inp[9] + 5

    # Digit 10
    x = z % 26 - 5
    z = z // 26
    if x != inp[10]:
        z = 26 * z + inp[10] + 9

    # Digit 11
    x = z % 26 - 10
    z = z // 26
    if x != inp[11]:
        z = 26 * z + inp[11] + 12

    # Digit 12
    x = z % 26 - 4
    z = z // 26
    if x != inp[12]:
        z = 26 * z + inp[12] + 14

    # Digit 13
    x = z % 26 - 5
    z = z // 26
    if x != inp[13]:
        z = 26 * z + inp[13] + 14

    return {"w": w, "x": x, "y": y, "z": z}

    # Same algo as used above:
    # w, x, y, z = 0, 0, 0, 0
    # for n in range(8, 14):
    #     if a[n] == 1:
    #         # Algo 1
    #         z = 26 * z + inp[n] + c[n]
    #     elif a[n] == 26:
    #         # Algo 2
    #         x = z % 26 + b[n]
    #         z = z // 26
    #         if x != inp[n]:
    #             z = 26 * z + inp[n] + c[n]
    #     else:
    #         raise Exception("Unknown algo")

    # return {"w": w, "x": x, "y": y, "z": z}


def solve(data):
    ops = parse(data)

    max_inp = [9, 2, 9, 1, 5, 9, 7, 9, 9, 9, 9, 4, 9, 8]
    min_inp = [2, 1, 6, 1, 1, 5, 1, 3, 9, 1, 1, 1, 8, 1]

    for inp in [max_inp, min_inp]:
        vm_z = run_vm(ops, inp)["z"]
        algo_z = run_algo(inp)["z"]
        print(f"{inp} -> vm: {vm_z}, algo: {algo_z}")
        assert vm_z == algo_z

    return 1


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Solution:")
solve(lines)
