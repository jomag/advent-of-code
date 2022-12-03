
def prio(c):
    if c.islower():
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27

def part1(data, verbose=False):
    p = 0
    for items in data:
        c1 = items[:len(items) // 2]
        c2 = items[len(items) // 2:]
        shared = set(c for c in c1 if c in c2)
        p += sum(prio(c) for c in shared)
    return p


def part2(data, verbose=False):
    groups = [data[n:n+3] for n in range(0, len(data), 3)]
    p = 0
    for g in groups:
        shared = set(c for c in g[0] if c in g[1] and c in g[2])
        p += sum(prio(c) for c in shared)
    return p


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
