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


def validate_seq(seq, data):
    next_subs = [data]

    for e in seq:
        subs = next_subs
        next_subs = []

        for sub in subs:
            if type(e) is str:
                if len(sub) > 0 and e == sub[0]:
                    next_subs.append(sub[1:])
            else:
                next_subs.extend(validate_rule(rules[e], sub))

    return next_subs


def validate_rule(rule, data):
    return [r for seq in rule for r in validate_seq(seq, data)]


def validate(rule, data):
    return any(len(r) == 0 for r in validate_rule(rule, data))


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


part1 = sum(1 for m in messages if validate(rules[0], m))
print(f"Part 1: {part1}")

rules[8] = [[42], [42, 8]]
rules[11] = [[42, 31], [42, 11, 31]]

part2 = sum(1 for m in messages if validate(rules[0], m))
print(f"Part 2: {part2}")
