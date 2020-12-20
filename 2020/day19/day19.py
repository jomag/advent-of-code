import sys


def add_rule(line: str):
    def num_or_str(s):
        if s[0] == '"':
            return s[1:-1]
        else:
            return int(s)

    name, rest = line.split(":")
    groups = rest.split("|")
    groups = [[num_or_str(s) for s in g.split() if s] for g in groups]
    rules[int(name)] = groups


def validate_seq(seq, data: str, indent):
    next_subs = [data]

    for e in seq:
        subs = [s for s in next_subs]
        next_subs = []

        for sub in subs:
            if type(e) is str:
                if len(sub) > 0 and e == sub[0]:
                    next_subs.append(sub[1:])
            else:
                next_subs.extend(validate_rule(e, sub, indent + "  "))

    return next_subs


def validate_rule(rule_id, data, indent=""):
    """Returns all possible remains after rule has been evaluated"""
    rule = rules[rule_id]
    remains = []

    for seq in rule:
        r = validate_seq(seq, data, indent + "  ")
        if r is not False:
            remains.extend(r)

    return remains


def validate(rule_id, substr):
    remains = validate_rule(rule_id, substr)
    return any(len(r) == 0 for r in remains)


rules = {}
messages = []

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    part = 0
    for line in f.readlines():
        line = line.strip()
        if line == "":
            part = 1
        elif part == 0:
            add_rule(line)
        else:
            messages.append(line)


part1 = sum(1 for m in messages if validate(0, m))
print(f"Part 1: {part1}")

rules[8] = [[42], [42, 8]]
rules[11] = [[42, 31], [42, 11, 31]]

part2 = sum(1 for m in messages if validate(0, m))
print(f"Part 2: {part2}")
