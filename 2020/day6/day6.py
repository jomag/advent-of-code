def solve(group, m):
    gs = set(group[0])
    for p in group[1:]:
        gs = m(gs, p)
    return gs


with open("input") as f:
    inp = f.readlines()

groups = []
group = []
for row in inp:
    row = row.strip()
    if row == "":
        groups.append(group)
        group = []
    else:
        group.append(set(row))
groups.append(group)

part1 = sum([len(solve(g, lambda a, b: a.union(b))) for g in groups])
print(f"Part 1: {part1}")

part2 = sum([len(solve(g, lambda a, b: a.intersection(b))) for g in groups])
print(f"Part 2: {part2}")
