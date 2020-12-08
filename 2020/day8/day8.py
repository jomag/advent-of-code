import sys, re


def run(prg):
    visits = set()
    acc = 0
    pc = 0
    while pc not in visits and pc != len(prg):
        visits.add(pc)
        op, val = prg[pc]
        if op == "acc":
            acc += val
        elif op == "jmp":
            pc += val - 1
        pc += 1
    return pc, acc


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    src = f.readlines()

prg = []
for line in src:
    m = re.match("(nop|acc|jmp)\s+([-+]\d+)", line)
    prg.append([m.group(1), int(m.group(2))])

pc, acc = run(prg)
print(f"Part 1: {acc}")

for i in range(len(prg)):
    op = prg[i][0]
    if op == "nop":
        prg[i][0] = "jmp"
    if op == "jmp":
        prg[i][0] = "nop"

    pc, acc = run(prg)
    if pc == len(prg):
        print(f"Part 2: instr {i} was '{op}'. acc: {acc}")
        break

    prg[i][0] = op
