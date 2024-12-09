def part1(data):
    disk = []
    last_used_block = 0
    first_empty_block = 0

    for i, c in enumerate(data):
        if i % 2 == 0:
            disk = disk + [int(i / 2)] * int(c)
            last_used_block = len(disk) - 1
        else:
            if first_empty_block == 0:
                first_empty_block = len(disk)
            disk = disk + [None] * int(c)

    while first_empty_block < last_used_block:
        disk[first_empty_block] = disk[last_used_block]
        disk[last_used_block] = None
        while disk[first_empty_block] is not None:
            first_empty_block += 1
        while disk[last_used_block] is None:
            last_used_block -= 1

    sum = 0
    for i, c in enumerate(disk):
        if c is None:
            break
        sum += i * int(c)

    return sum


def part2(data):
    disk = []

    for i, c in enumerate(data):
        if i % 2 == 0:
            if int(c) > 0:
                disk.append((int(i / 2), int(c)))
        else:
            if int(c) > 0:
                disk.append((None, int(c)))

    files_in_order = [f[0] for f in reversed(disk) if f[0] is not None]

    def find_unused_segment_with_size(sz):
        for i, f in enumerate(disk):
            if f[0] is None and f[1] >= sz:
                return i

    def find_file(name):
        for i, f in enumerate(disk):
            if f[0] == name:
                return i, f[1]
        raise Exception("File not found")

    for name in files_in_order:
        pos, size = find_file(name)
        to = find_unused_segment_with_size(size)
        if to is None or to > pos:
            continue
        if disk[to][1] == size:
            disk[pos] = (None, size)
            disk[to] = (name, size)
        else:
            disk[pos] = (None, size)
            empty_size = disk[to][1]
            assert empty_size > size
            disk[to] = (name, size)
            disk.insert(to + 1, (None, empty_size - size))

    sum = 0
    blk = 0
    for i, c in enumerate(disk):
        key, cnt = c
        if key is None:
            blk += cnt
        else:
            for _ in range(cnt):
                sum += blk * key
                blk = blk + 1

    return sum


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

example = "2333133121414131402"

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines[0])}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines[0])}")
