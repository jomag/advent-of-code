import sys


def solve1(path):
    def rec(path):
        jolt = path[-1]
        for n in [1, 2, 3]:
            if jolt + n in adapters:
                diff[n - 1] += 1
                return rec(path + [jolt + n])

    diff = [0, 0, 0]
    rec(path)
    return diff


def solve2(jolt, target, remaining):
    def rec(jolt, remaining):
        if jolt == target:
            return 1

        if remaining in visited:
            return visited[remaining]

        n = 0

        for diff in [1, 2, 3]:
            if jolt + diff in remaining:
                sub = frozenset([a for a in remaining if a > jolt + diff])
                n += rec(jolt + diff, sub)

        visited[remaining] = n
        return n

    visited = {}
    return rec(jolt, frozenset(remaining))


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    adapters = set([int(line) for line in f.readlines()])

adapters.add(max(adapters) + 3)

res = solve1([0])
assert res is not None, "No solution found"
print(f"Part 1:\n - {res[0]} diff of 1\n - {res[1]} diff of 2\n - {res[2]} diff of 3")
print(f" - Solution: {res[2] * res[0]}")

n = solve2(0, max(adapters), adapters)
print(f"Part 2:\n - {n} solutions")
