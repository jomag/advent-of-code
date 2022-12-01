
elves = []
cur = 0

with open("input.txt") as f:
    for ln in f.readlines():
        try:
            cur += int(ln)
        except ValueError:
            elves.append(cur)
            cur = 0

elves.append(cur)
elves = sorted(elves, reverse=True)

print(f"Part 1: {elves[0]}")
print(f"Part 2: {sum(elves[0:3])}")
