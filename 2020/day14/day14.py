import sys, re


def part1(prg):
    mem = {}
    mask0, mask1 = 0, 0

    for op in prg:
        if op[0] == "mask":
            mask0, mask1 = 0, 0
            for c in op[1]:
                if c == "1":
                    mask0 = mask0 << 1
                    mask1 = (mask1 << 1) | 1
                elif c == "0":
                    mask0 = (mask0 << 1) | 1
                    mask1 = mask1 << 1
                else:
                    mask0 = mask0 << 1
                    mask1 = mask1 << 1
        if op[0] == "mem":
            val = (op[2] | mask1) & ~mask0
            mem[op[1]] = val
    return sum(mem.values())


def part2(prg):
    def permutations(maskx):
        perm = []
        for bit in range(36):
            if maskx & (1 << bit) != 0:
                if not perm:
                    perm = [0, (1 << bit)]
                else:
                    p = []
                    for x in perm:
                        p.append(x & ~(1 << bit))
                        p.append(x | (1 << bit))
                    perm = p
        return perm

    mem = {}
    mask0, mask1, maskx = 0, 0, 0

    for op in prg:
        if op[0] == "mask":
            mask0, mask1, maskx = 0, 0, 0
            for c in op[1]:
                mask0 <<= 1
                mask1 <<= 1
                maskx <<= 1
                if c == "1":
                    mask1 |= 1
                elif c == "0":
                    mask0 |= 1
                elif c == "X":
                    maskx |= 1
        if op[0] == "mem":
            a = op[1] | mask1
            adrx = permutations(maskx)
            for p in adrx:
                mem[p | (a & ~maskx)] = op[2]

    return sum(mem.values())


prg = []
filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    for line in f.readlines():
        m = re.match(r"mask\s*=\s*([01X]+)", line)
        if m:
            prg.append(("mask", m.group(1)))

        m = re.match(r"mem\[(\d+)\]\s*=\s*(\d+)", line)
        if m:
            prg.append(("mem", int(m.group(1)), int(m.group(2))))

print(f"Part 1: {part1(prg)}")
print(f"Part 2: {part2(prg)}")
