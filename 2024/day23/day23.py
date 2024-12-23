import time


def parse(data):
    pairs = [tuple(line.split("-")) for line in data if line]
    return pairs


def part1(data):
    pairs = [p for p in data]

    computers = set()
    for p in pairs:
        computers.add(p[0])
        computers.add(p[1])

    conn = {}
    for c in computers:
        o = set()
        for p in pairs:
            if p[0] == c or p[1] == c:
                o.add(p[0])
                o.add(p[1])
        o.remove(c)
        conn[c] = o

    threes = set()

    for c1, o in conn.items():
        for c2 in o:
            for c3 in o:
                if c2 == c3:
                    continue
                if c3 in conn[c2]:
                    grp = sorted([c1, c2, c3])
                    threes.add(tuple(grp))

    threes = set([g for g in threes if "t" in (g[0][0], g[1][0], g[2][0])])

    return len(threes)


def part2(data):
    pairs = [p for p in data]
    computers = set()

    for p in pairs:
        computers.add(p[0])
        computers.add(p[1])

    conn = {}
    for c in computers:
        o = set()
        for p in pairs:
            if p[0] == c or p[1] == c:
                o.add(p[0])
                o.add(p[1])
        o.remove(c)
        conn[c] = o

    groups = set([(c,) for c in computers])

    m = True
    while m:
        remove_list = set()
        add_list = set()
        for c in computers:
            for grp in groups:
                for c2 in grp:
                    if c2 not in conn[c]:
                        break
                else:
                    new_group = tuple(sorted([*grp, c]))
                    add_list.add(new_group)
                    remove_list.add(grp)
        for g in remove_list:
            groups.remove(g)
        for g in add_list:
            groups.add(g)
        m = len(remove_list) + len(add_list)

    longest = ()
    for t in groups:
        if len(t) > len(longest):
            longest = t

    return ",".join(longest)


def run(label, f):
    start = time.perf_counter()
    result = f()
    elapsed = time.perf_counter() - start
    if elapsed > 2:
        elapsed = f"{elapsed:.3f}s"
    else:
        elapsed = f"{elapsed*1000:.1f}ms"
    print(f"{label}: {result} ({elapsed})")


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

run("Part 1 with example data", lambda: part1(example))
run("Part 1 with real input", lambda: part1(lines))
run("Part 2 with example data", lambda: part2(example))
run("Part 2 with real input", lambda: part2(lines))
