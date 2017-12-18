
from pprint import pprint


def parse(text):
    ops = [line.split() for line in text.splitlines() if line]
    assert all(len(op) == 7 for op in ops)
    return ops
    

def run(ops):
    highest = None
    registers = {}
    for op in ops:
        try:
            lh = registers[op[4]]
        except:
            lh = 0
        rh = int(op[6])
        trg = op[0]
        cmd = op[1]
        val = int(op[2])

        if op[5] == ">":
            do = lh > rh
        elif op[5] == "<":
            do = lh < rh
        elif op[5] == ">=":
            do = lh >= rh
        elif op[5] == "<=":
            do = lh <= rh
        elif op[5] == "==":
            do = lh == rh
        elif op[5] == "!=":
            do = lh != rh
        else:
            raise RuntimeError("Invalid operator: " + op[5])
        
        if do:
            if cmd == "inc":
                try:
                    registers[trg] = registers[trg] + val
                except:
                    registers[trg] = val
            elif cmd == "dec":
                try:
                    registers[trg] = registers[trg] - val
                except:
                    registers[trg] = -val
            else:
                raise RuntimeError("Invalid command: " + cmd)
            if highest is None or registers[trg] > highest:
                highest = registers[trg]

    return registers, highest


example = """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""

ops = parse(example)
regs, highest = run(ops)
pprint(regs)
print("Highest: %d" % highest)
print("Max: %d\n" % max(regs.values()))

with open("day8.txt") as f:
    input_data = f.read()

ops = parse(input_data)
regs, highest = run(ops)
pprint(regs)
print("Highest: %d" % highest)
print("Max: %d" % max(regs.values()))


