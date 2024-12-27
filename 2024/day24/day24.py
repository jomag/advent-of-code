import time

# This was a frustrating puzzle, especially on the
# 24'th of december, the day we celebrate christmas
# in Sweden!
#
# Part 1 was straight forward and easy to solve.
#
# Part 2 however was a mess and took a lot of different
# strategies before I found what worked. At first I tried
# to brute force by swapping all rules, but there are
# way too many rules for this to work. So I tried to
# narrow down the number of rules by first checking
# which bits was buggy. It turned out there was four
# such bits, so I tested brute forcing only the rules
# used to evaluate those, hoping that the puzzle was
# setup in such a way (since there are four swaps that
# needs to happen, and four bits that were wrong, it
# seemed likely). This approach took several seconds
# to run, and returned swaps that worked for the input
# values of x and y for two of the bits. But x+y=z
# should be true for all values of x and y (I missed
# this at first), and when testing other values they
# still did not work.
#
# Finally, I visualized the trees, first in terminal,
# but finally using Graphviz. I could focus on the
# suspicious bits I had found earlier, and analyzed
# those bits, plus one bit before and after, and
# could quite quickly find the needed swaps.
#
# I considered writing a solver for part 2 given
# the learnings from above, but the solver would
# be very dependent on the input (for example,
# any solver I could think of would break if
# no-ops were introduced in the input), so I
# decided to not bother.

def parse(data):
    n = 0
    wires = {}
    rules = {}
    while data[n] != "":
        wire, state = data[n].split(":")
        wires[wire] =bool (int(state))
        n += 1
    n += 1
    while n < len(data):
        stmt,r = data[n].split("->")
        stmt = tuple([o.strip() for o in stmt.split()])
        r = r.strip()
        assert r not in rules
        rules[r]=stmt
        n+=1

    return wires, rules

def part1(data):
    initial, rules = data

    def get_value_for(w):
        if w in initial:
            return initial[w]
        stmt = rules[w]
        a, op, b = stmt
        a = get_value_for(a)
        b = get_value_for(b)
        if op == "AND":
            return a and b
        elif op == "OR":
            return a or b
        elif op == "XOR":
            return (a and not b) or (b and not a)
        else:
            raise Exception(f"Invalid op: {op}")

    zv = reversed(sorted([k for k in rules if k[0] == "z"]))

    v = 0
    for name in zv:
        if get_value_for(name):
            v = (v << 1) | 1
        else:
            v = (v << 1)

    return v

def deps_for(k, rules):
    if rules[k] is None:
        return {k}

    a, _, b = rules[k]
    deps = {k}
    deps.update(deps_for(a,rules))
    deps.update(deps_for(b,rules))
    return deps
    
    
def print_rule_tree(rule, ruleset, indent=""):
    if rule in ruleset:
        if ruleset[rule] is None:
            print(f"{indent}{rule}.")
            return
        print(f"{indent}{rule}:")
        a, op, b = ruleset[rule]
        indent += "  "
        if ruleset[a] is None and ruleset[b] is None:
            if ruleset[b] < ruleset[a]:
                a,b = b,a
        elif ruleset[b][1] < ruleset[a][1]:
            a, b = b, a
        print_rule_tree(a, ruleset, indent)
        print(f"{indent}{op}")
        print_rule_tree(b, ruleset, indent)
    else:
        print(f"{indent}{rule}")
    
def visualize_rule(r, rules):
    deps = deps_for(r, rules)
    deps.add(r)

    dot = ["digraph G {", f"{r};"]

    for dep in deps:
        stmt = rules[dep]
        if stmt is None:
            pass
            # label = dep
        else:
            a, op, b = stmt
            # label = f"{dep}\n{op}"
            dot.append(f'{dep} [label="{dep}\\n{op}"];')
            dot.append(f"{dep} -> {a};")
            dot.append(f"{dep} -> {b};")

    dot.append("}")

    with open(f"vis_{r}.dot", "w") as f:
        f.writelines(dot)



class Part2:
    def __init__(self, data):
        _, self.init_rules = data
        self.x = 0
        self.y = 0

    def get_value_for(self, w, rules, visited=[]):
        if w in visited:
            return None

        if w[0] == "x":
            bit = int(w[1:])
            return self.x & (1 << bit) != 0
        if w[0] == "y":
            bit = int(w[1:])
            return self.y & (1 << bit) != 0

        stmt = rules[w]

        if stmt is None:
            raise Exception(f"Invalid empty statement for rule {w}")
                
        a, op, b = stmt
        a = self.get_value_for(a, rules,[*visited,w])
        b = self.get_value_for(b,rules, [*visited,w])

        if a is None or b is None:
            return None
        if op == "AND":
            return a and b
        elif op == "OR":
            return a or b
        elif op == "XOR":
            return (a and not b) or (b and not a)
        else:
            raise Exception(f"Invalid op: {op}")

    def get_number(self,prefix:str, rules):
        if prefix == "x":
            return self.x
        if prefix == "y":
            return self.y

        names = rules.keys()
        bits = list(reversed(sorted([k for k in names if k[0] == prefix])))
        v = 0
        for bit in bits:
            if self.get_value_for(bit,rules):
                v = (v << 1) | 1
            else:
                v = (v << 1)
        return v

    def find_suspicious_bits(self):
        def validate_bit(n,rules):
            bit = 1 <<n
            for x,y,z in [(0,0,0),(0,bit,bit),(bit,0,bit),(bit,bit,0)]:
                self.x = x
                self.y = y
                v = self.get_number("z", rules)
                if v is None or v & bit != z:
                    return False
            return True

        sus_bits = set()
        for n in range(45):
            if not validate_bit(n, self.init_rules):
                sus_bits.add(n)
        return sorted(sus_bits)

def run(label, f):
    start = time.perf_counter()
    result = f()
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

run("Part 1 with example data", lambda: part1(example))
run("Part 1 with real input", lambda: part1(lines))

p2 = Part2(lines)

# print("Suspicious bits in part 2:", ", ".join(map(str, p2.find_suspicious_bits())))
swaps = [("ggn","z10"),("jcb","ndw"),("z32","grm"),("z39","twr")]
part2 = ",".join(sorted([a[0] for a in swaps] + [a[1] for a in swaps]))
print("Part 2:", part2)
