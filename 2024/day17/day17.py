import time
from enum import Enum


class Op(Enum):
    ADV = 0  # Division (A div 2^combo -> A)
    BXL = 1  # Bitwise XOR (B xor literal -> B)
    BST = 2  # Modulo (combo % 8 -> B)
    JNZ = 3  # Jump if not zero (A != 0 => PC = literal)
    BXC = 4  # Bitwise XOR (B xor C -> B)
    OUT = 5  # Output (combo % 8 -> output)
    BDV = 6  # Division (A div 2^combo -> B)
    CDV = 7  # Division (A div 2^combo -> C)


def parse(data):
    n = 0
    regs = {}
    while n < len(data) and data[n] != "":
        r, v = data[n].split(":")
        regs[r[-1]] = int(v)
        n += 1
    prefix, prg = data[n + 1].split(":")
    assert prefix == "Program"
    prg = tuple(map(int, prg.split(",")))
    return regs, prg


def interpret(prg, a=0, b=0, c=0):
    pc = 0
    out = []

    def combo(o):
        match o:
            case v if v in [0, 1, 2, 3]:
                return v
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case _:
                raise Exception("Invalid combo operand")

    debug = False

    while pc < len(prg):
        op = prg[pc]

        if op != Op.JNZ.value:
            if len(prg) <= pc + 1:
                break
            v = prg[pc + 1]
        else:
            v = 0

        if debug:
            print(f"State: A={a} B={b} C={c} PC={pc} OUT={out}. Next op: {op} ({v})")
            input()

        match op:
            case Op.ADV.value:
                a = a // (2 ** combo(v))
            case Op.BXL.value:
                b = b ^ v
            case Op.BST.value:
                b = combo(v) % 8
            case Op.JNZ.value:
                if a != 0:
                    pc = v
                else:
                    pc += 1
            case Op.BXC.value:
                b = b ^ c
            case Op.OUT.value:
                out.append(combo(v) % 8)
            case Op.BDV.value:
                b = a // (2 ** combo(v))
            case Op.CDV.value:
                c = a // (2 ** combo(v))
            case _:
                raise Exception(f"Invalid operator: {op} ({type(op)})")

        if op != Op.JNZ.value:
            pc += 2

    if debug:
        print(f"Final state: A={a} B={b} C={c} PC={pc} OUT={out}")
    return out


def part1(data):
    regs, prg = data
    return ",".join(map(str, interpret(prg, a=regs["A"], b=regs["B"], c=regs["C"])))


def part2(data):
    def test_digit_n(n, prg):
        if len(prg) == n:
            return [0]

        upper_valids = test_digit_n(n + 1, prg)
        valids = []
        sub = prg[n:]

        for i in range(0, 8):
            for upper in upper_valids:
                a = (upper << 3) | i
                if interpret(prg, a=a) == list(sub):
                    valids.append(a)

        return valids

    return min(test_digit_n(0, data[1]))


def run(label, f, data):
    start = time.perf_counter()
    result = f(data)
    elapsed = time.perf_counter() - start
    if elapsed > 2:
        elapsed = f"{elapsed:.3f}s"
    else:
        elapsed = f"{elapsed*1000:.1f}ms"
    print(f"{label}: {result} ({elapsed})")


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

run("Part 1 with example data", part1, example)
run("Part 1 with real input", part1, lines)
run("Part 2 with real input", part2, lines)
