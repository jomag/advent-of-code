import re


def find_seat(inp: str):
    def partition(path, a, b):
        if len(path) == 0:
            return a
        if path[0] in ["F", "L"]:
            return partition(path[1:], a, a + (b - a) // 2)
        else:
            return partition(path[1:], a + (b - a) // 2, b)

    m = re.match("^([BF]{7})([LR]{3})$", inp)
    if not m:
        raise Exception(f"Invalid input: {inp}")

    row_path, col_path = m.groups()
    row = partition(row_path, 0, 128)
    col = partition(col_path, 0, 8)
    return row, col, row * 8 + col


with open("input") as f:
    bps = f.readlines()

bps = [find_seat(bp) for bp in bps]
bps = sorted(bps, key=lambda bp: bp[2])

part1 = max(bp[2] for bp in bps)
print(f"Part 1: {part1}")

i = bps[0][2]
non_consecutives = []
for bp in bps[1:]:
    if i + 1 != bp[2]:
        non_consecutives.append(i + 1)
    i = bp[2]

if len(non_consecutives) != 1:
    raise Exception(f"More than one consecutive found: {non_consecutives}")

print(f"Part 2: {non_consecutives[0]}")
