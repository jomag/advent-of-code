def parse(data):
    n = data.index("")
    rules, updates = data[:n], data[n + 1 :]
    rules = [rule.split("|") for rule in rules]
    rules = [(int(r[0]), int(r[1])) for r in rules]
    updates = [update.split(",") for update in updates]
    updates = [[int(p) for p in update] for update in updates]
    return (rules, updates)


def sort_update(upd, rules):
    def find_first(u):
        p = u[0]
        while True:
            for r1, r2 in rules:
                if r2 == p and r1 in u:
                    p = r1
                    break
            else:
                return p

    su = []
    upd = upd[:]
    while len(upd) > 0:
        p = find_first(upd)
        su.append(p)
        upd.remove(p)

    return su


def part1(data):
    rules, updates = data

    tot = 0
    for update in updates:
        if sort_update(update, rules) == update:
            tot += update[int(len(update) / 2)]

    return tot


def part2(data):
    rules, updates = data

    tot = 0
    for update in updates:
        sorted_update = sort_update(update, rules)
        if sorted_update != update:
            tot += sorted_update[int(len(sorted_update) / 2)]

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
