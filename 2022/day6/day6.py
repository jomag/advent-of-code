def solve(data, sz):
    buf = data[: sz - 1]
    for n in range(sz - 1, len(data)):
        buf = buf[-(sz - 1) :] + data[n]
        if len(set(buf)) == sz:
            return n + 1


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data:")
for ln in example:
    print(f" - {ln}: {solve(ln,4)}")

print(f"Part 1 with real input:")
for ln in lines:
    print(f" - {ln[:20]}...: {solve(ln,4)}")

print(f"Part 2 with example data:")
for ln in example:
    print(f" - {ln}: {solve(ln, 14)}")

print(f"Part 2 with real input:")
for ln in lines:
    print(f" - {ln[:20]}...: {solve(ln, 14)}")
