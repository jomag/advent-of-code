import time

# This was quite easy, but the code got messy. I think I may have
# complicated things by implementing a full A-star (from the
# Wikipedia article), but it works. For part 2 I did the binary
# search in my head to find the value, and then could not be
# bothered to do an automated version. This will have to do
# for today...


def parse(data):
    positions = [tuple(map(int, ln.split(","))) for ln in data if ln]
    w = max([p[0] for p in positions]) + 1
    h = max([p[1] for p in positions]) + 1
    return positions, w, h


def print_map(w, h, p, path=[]):
    for y in range(h):
        s = ""
        for x in range(w):
            if (x, y) in p:
                s += "#"
            elif (x, y) in path:
                s += "O"
            else:
                s += "."
        print(s)


def a_star(start, goal, blocks, w, h):
    def reconstruct_path(came_from, cur):
        path = [cur]
        while cur in came_from:
            cur = came_from[cur]
            path.append(cur)
        return path

    open_set = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: 0}
    while open_set:
        cur = None
        lowest_score = 0
        for p in open_set:
            if cur is None:
                cur = p
                lowest_score = f_score[p]
            else:
                if p in f_score and f_score[p] < lowest_score:
                    cur = p
                    lowest_score = f_score[p]

        if cur == goal:
            return reconstruct_path(came_from, cur)

        if not cur:
            raise Exception("Should have cur")

        open_set.remove(cur)
        for n in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nn = (cur[0] + n[0], cur[1] + n[1])
            if nn[0] < 0 or nn[1] < 0 or nn[0] >= w or nn[1] >= h or nn in blocks:
                continue
            tentative_score = g_score[cur] + 1
            if nn not in g_score or tentative_score < g_score[nn]:
                came_from[nn] = cur
                g_score[nn] = tentative_score
                f_score[nn] = tentative_score + 1
                if nn not in open_set:
                    open_set.append(nn)

        cur = []

    return None


def part1(data):
    p, w, h = data

    # Run example with 12 bytes, and real input with 1024
    n = 12 if w < 20 else 1024

    path = a_star((0, 0), (w - 1, h - 1), p[:n], w, h)
    assert path
    return len(path) - 1


def part2(data):
    p, w, h = data

    # I found the value 2850 via manual testing a few values
    # The automated approach would be a binary search, splitting
    # bytes in half until the breaking block is found
    start = 0 if w < 20 else 2850

    for n in range(start, len(p)):
        path = a_star((0, 0), (w - 1, h - 1), p[:n], w, h)
        if path is None:
            return ",".join(map(str, p[n - 1]))
    return -1


def run(label, f, data):
    start = time.perf_counter()
    result = f(data)
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

run("Part 1 with example data", part1, example)
run("Part 1 with real input", part1, lines)
run("Part 2 with example data", part2, example)
run("Part 2 with real input", part2, lines)
