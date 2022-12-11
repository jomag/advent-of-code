class Entry:
    def __init__(self, size=0):
        self.size = size
        self.content = {}

    def total_size(self) -> int:
        return self.size + sum(v.total_size() for v in self.content.values())


def part1(data, verbose=False):
    root = Entry()
    path = []

    exec = False

    def find_entry(p):
        e = root
        for s in p:
            e = e.content[s]
        return e

    for line in data:
        cmd = line.split()
        if cmd[0] == "$":
            exec = False
            if cmd[1] == "cd":
                if cmd[2] == "/":
                    path = []
                elif cmd[2] == "..":
                    path = path[:-1]
                else:
                    path.append(cmd[2])
            elif cmd[1] == "ls":
                exec = True
        elif exec:
            assert len(cmd) == 2
            sz, name = cmd
            e = find_entry(path)
            if name not in e.content:
                if sz == "dir":
                    e.content[name] = Entry()
                else:
                    e.content[name] = Entry(int(sz))

    dirsum = 0

    def rec(e):
        nonlocal dirsum
        for v in e.content.values():
            if v.size == 0:
                totsz = v.total_size()
                if totsz < 100000:
                    dirsum += totsz
                rec(v)

    rec(root)
    return dirsum


def part2(data, verbose=False):
    root = Entry()
    path = []

    exec = False

    def find_entry(p):
        e = root
        for s in p:
            e = e.content[s]
        return e

    for line in data:
        cmd = line.split()
        if cmd[0] == "$":
            exec = False
            if cmd[1] == "cd":
                if cmd[2] == "/":
                    path = []
                elif cmd[2] == "..":
                    path = path[:-1]
                else:
                    path.append(cmd[2])
            elif cmd[1] == "ls":
                exec = True
        elif exec:
            assert len(cmd) == 2
            sz, name = cmd
            e = find_entry(path)
            if name not in e.content:
                if sz == "dir":
                    e.content[name] = Entry()
                else:
                    e.content[name] = Entry(int(sz))

    bigdirs = []
    req = 30000000
    disksz = 70000000
    free_bytes = disksz - root.total_size()
    min_freed = req - free_bytes

    def rec(e):
        nonlocal bigdirs
        for v in e.content.values():
            if v.size == 0:
                totsz = v.total_size()
                if totsz >= min_freed:
                    bigdirs.append(totsz)
                rec(v)

    rec(root)

    return sorted(bigdirs)[0]


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
