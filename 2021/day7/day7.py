# For the second part, I first did a quite verbose cost table algorithm.
# After inspecting the costs, I found that they are "triangular numbers":
# https://en.wikipedia.org/wiki/Triangular_number.


def solve(positions, cost):
    a, b = min(positions), max(positions)
    return min([sum([cost(abs(c - p)) for c in positions]) for p in range(a, b + 1)])


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]
    lines = [int(i) for i in lines[0].split(",")]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]
    example = [int(i) for i in example[0].split(",")]

cost1 = lambda n: n
cost2 = lambda n: (n * (n + 1)) // 2

print(f"Part 1 with example data: {solve(example, cost1)}")
print(f"Part 1 with real input: {solve(lines, cost1)}")
print(f"Part 2 with example data: {solve(example, cost2)}")
print(f"Part 2 with real input: {solve(lines, cost2)}")
