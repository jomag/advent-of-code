def find_paths(conn, allow_revisit):
    paths = []
    visited = set()

    def rec(at, path, revisited=False):
        nonlocal paths
        nonlocal visited

        if at == "end":
            paths.append(path + [at])
            return

        first_visit = at not in visited
        revisited = revisited or not first_visit
        if at.islower():
            visited.add(at)

        for cave in conn[at]:
            if cave != "start":
                if cave not in visited or (allow_revisit and not revisited):
                    rec(cave, [p for p in path] + [at], revisited)

        if at.islower() and first_visit:
            visited.remove(at)

    rec("start", [])
    return paths


def solve(data, allow_revisit, verbose=False):
    conn = {}

    for line in data:
        a, b = line.split("-")
        try:
            conn[a].add(b)
        except KeyError:
            conn[a] = set([b])
        try:
            conn[b].add(a)
        except KeyError:
            conn[b] = set([a])

    paths = find_paths(conn, allow_revisit)

    if verbose:
        s = []
        for p in paths:
            s.append(" -> ".join(p))
        for p in sorted(s):
            print(p)

    return len(paths)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {solve(example, False, verbose=True)}")
print(f"Part 1 with real input: {solve(lines, False)}")
# print(f"Part 2 with example data: {solve(example, True, verbose=True)}")
print(f"Part 2 with real input: {solve(lines, True)}")
