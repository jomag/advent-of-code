with open("input") as f:
    lines = f.readlines()

depths = [int(line) for line in lines]

prev = None
count = 0
for d in depths:
    if prev is not None and d > prev:
        count += 1
    prev = d

print(f"Part 1: {count}")

example = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

prev = None
count = 0
for i in range(len(depths)):
    grp = sum(depths[i : i + 3])
    if prev is not None and grp > prev:
        count += 1
    prev = grp

print(f"Part 2: {count}")
