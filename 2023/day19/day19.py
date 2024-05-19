import re

# 167409079868000


def part1(data, verbose=False):
    workflows = {}
    parts = []
    flow_re = re.compile(r"([a-z]+)\{(.*)\}")
    rule_re = re.compile(r"([xmas])([<>])(\d+):([a-zRA]+)")

    while data:
        flow = data.pop(0)
        if flow == "":
            break

        m = flow_re.match(flow)
        assert m
        name, rules = m.groups()
        rules = rules.split(",")

        flow_rules = []
        for r in rules:
            m = rule_re.match(r)
            if m:
                flow_rules.append((m.group(1), m.group(2), int(m.group(3)), m.group(4)))
            else:
                flow_rules.append((r,))

        workflows[name] = flow_rules

    for line in data:
        part = {}
        ratings = line[1:-1].split(",")
        for r in ratings:
            name, value = r.split("=")
            part[name] = int(value)
        parts.append(part)

    print("Workflows:")
    print(workflows)
    print("\nParts:")
    print(parts)

    tot = 0
    for part in parts:
        print(f"Evaluate part: {part}")
        flow_name = "in"
        while flow_name != "R" and flow_name != "A":
            flow = workflows[flow_name]
            print(f"  - Testing flow {flow_name}: {flow}")
            for rule in flow:
                if len(rule) == 1:
                    flow_name = rule[0]
                elif rule[1] == ">":
                    if part[rule[0]] > rule[2]:
                        flow_name = rule[3]
                        break
                elif rule[1] == "<":
                    if part[rule[0]] < rule[2]:
                        flow_name = rule[3]
                        break
                else:
                    raise Exception(f"Invalid rule: {rule}")
                print(f"    - Rule {rule} -> {flow_name}")

        if flow_name == "A":
            print("Accepted!")
            tot += sum(part.values())
        elif flow_name == "R":
            print("Rejected!")

    return tot


class Range:
    min: int
    max: int

    def __init__(self):
        self.min = 1
        self.max = 4000

    def clone(self):
        r = Range()
        r.min = self.min
        r.max = self.max
        return r

    def min_limit(self, value):
        self.min = max(self.min, value)

    def max_limit(self, value):
        self.max = min(self.max, value)

    def __repr__(self):
        return f"Range({self.min} - {self.max})"

    def count(self):
        return self.max - self.min + 1


def part2(data, verbose=False):
    workflows = {}
    flow_re = re.compile(r"([a-z]+)\{(.*)\}")
    rule_re = re.compile(r"([xmas])([<>])(\d+):([a-zRA]+)")

    while data:
        flow = data.pop(0)
        if flow == "":
            break

        m = flow_re.match(flow)
        assert m
        name, rules = m.groups()
        rules = rules.split(",")

        flow_rules = []
        for r in rules:
            m = rule_re.match(r)
            if m:
                flow_rules.append((m.group(1), m.group(2), int(m.group(3)), m.group(4)))
            else:
                flow_rules.append((r,))

        workflows[name] = flow_rules

    def build_tree(flow):
        rule = flow[0]
        if len(rule) == 1:
            if rule[0] in ["A", "R"]:
                return rule[0]
            else:
                return build_tree(workflows[rule[0]])

        if rule[3] in ["A", "R"]:
            return (rule[0:3], rule[3], build_tree(flow[1:]))
        else:
            return (rule[0:3], build_tree(workflows[rule[3]]), build_tree(flow[1:]))

    flow = workflows["in"]
    r = build_tree(flow)

    def print_tree(tree, indent=""):
        if tree == "A":
            print(f"{indent}ACCEPTED!")
        elif tree == "R":
            print(f"{indent}REJECTED!")
        else:
            print(f"{indent}IF {tree[0][0]} {tree[0][1]} {tree[0][2]}:")
            print_tree(tree[1], indent + "    ")
            print(f"{indent}ELSE:")
            print_tree(tree[2], indent + "    ")

    accept_criterias = []

    def find_criterias(tree, ranges):
        if tree == "A":
            accept_criterias.append(ranges)
            return
        if tree == "R":
            return

        prop, cond, val = tree[0]
        val = int(val)

        if cond == ">":
            true_ranges = ranges.copy()
            false_ranges = ranges.copy()
            true_ranges[prop] = ranges[prop].clone()
            true_ranges[prop].min_limit(val + 1)
            false_ranges[prop] = ranges[prop].clone()
            false_ranges[prop].max_limit(val)
            find_criterias(tree[1], true_ranges)
            find_criterias(tree[2], false_ranges)
        elif cond == "<":
            true_ranges = ranges.copy()
            false_ranges = ranges.copy()
            true_ranges[prop] = ranges[prop].clone()
            true_ranges[prop].max_limit(val - 1)
            false_ranges[prop] = ranges[prop].clone()
            false_ranges[prop].min_limit(val)
            find_criterias(tree[1], true_ranges)
            find_criterias(tree[2], false_ranges)
        else:
            raise Exception(f"Invalid condition: {cond}")

    find_criterias(r, {"x": Range(), "m": Range(), "a": Range(), "s": Range()})

    print_tree(r)

    tot = 0
    for c in accept_criterias:
        print(c)
        t = 1
        for v in c.values():
            t = t * v.count()
        tot += t
    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
