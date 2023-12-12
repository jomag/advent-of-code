def find_start(data):
    for y in range(len(data)):
        line = data[y]
        for x in range(len(line)):
            if line[x] == "S":
                return (x, y)


def part1(data, verbose=False):
    w, h = len(data[0]), len(data)
    start = find_start(data)
    assert start
    visited = set([start])

    def at(x, y):
        if y < 0 or y >= h or x < 0 or x >= w:
            return "."
        else:
            return data[y][x]

    def is_visited(x, y):
        return (x, y) in visited

    x1, y1 = start
    x2, y2 = start

    if at(x1, y1 - 1) in "|7F":
        y1 -= 1
    elif at(x1 + 1, y1) in "-J7":
        x1 += 1
    elif at(x1, y1 + 1) in "|JL":
        y1 += 1
    elif at(x1 - 1, y1) in "-LF":
        x1 -= 1
    visited.add((x1, y1))

    if at(x2, y2 - 1) in "|7F" and not is_visited(x2, y2 - 1):
        y2 -= 1
    elif at(x2 + 1, y2) in "-J7" and not is_visited(x2 + 1, y2):
        x2 += 1
    elif at(x2, y2 + 1) in "|JL" and not is_visited(x2, y2 + 1):
        y2 += 1
    elif at(x2 - 1, y2) in "-LF" and not is_visited(x2 - 1, y2):
        x2 -= 1
    visited.add((x2, y2))

    print(f"Step 1 positions: {x1}, {y1} | {x2}, {y2} | {visited}")

    def move_to_next(x, y):
        possibilities = {
            "-": [(x - 1, y), (x + 1, y)],
            "|": [(x, y - 1), (x, y + 1)],
            "7": [(x - 1, y), (x, y + 1)],
            "F": [(x + 1, y), (x, y + 1)],
            "L": [(x, y - 1), (x + 1, y)],
            "J": [(x - 1, y), (x, y - 1)],
            "S": [],
        }
        for dx, dy in possibilities[at(x, y)]:
            if not is_visited(dx, dy):
                return dx, dy
        raise Exception(f"No way out! {x}, {y}")

    distance = 1
    while x1 != x2 or y1 != y2:
        distance += 1
        print(f"POS: {x1} {y1} | {x2} {y2}")
        x1, y1 = move_to_next(x1, y1)
        x2, y2 = move_to_next(x2, y2)
        if x1 == x2 and y1 == y2:
            break
        visited.add((x1, y1))
        visited.add((x2, y2))

    return distance


def part2(orig_data, verbose=False):
    prepost = list("." * (len(orig_data[0]) + 2))
    data = [prepost] + [list("." + line + ".") for line in orig_data] + [prepost]
    for line in data:
        print("".join(line))

    w, h = len(data[0]), len(data)
    start = find_start(data)
    assert start
    visited = set([start])

    def at(x, y):
        if y < 0 or y >= h or x < 0 or x >= w:
            return "."
        else:
            return data[y][x]

    def is_visited(x, y):
        return (x, y) in visited

    x1, y1 = start
    x2, y2 = start

    if at(x1, y1 - 1) in "|7F":
        y1 -= 1
    elif at(x1 + 1, y1) in "-J7":
        x1 += 1
    elif at(x1, y1 + 1) in "|JL":
        y1 += 1
    elif at(x1 - 1, y1) in "-LF":
        x1 -= 1
    visited.add((x1, y1))

    if at(x2, y2 - 1) in "|7F" and not is_visited(x2, y2 - 1):
        y2 -= 1
    elif at(x2 + 1, y2) in "-J7" and not is_visited(x2 + 1, y2):
        x2 += 1
    elif at(x2, y2 + 1) in "|JL" and not is_visited(x2, y2 + 1):
        y2 += 1
    elif at(x2 - 1, y2) in "-LF" and not is_visited(x2 - 1, y2):
        x2 -= 1
    visited.add((x2, y2))

    sx, sy = start
    if x1 != x2 and y1 == y2:
        data[sy][sx] = "-"
    elif x1 == x2 and y1 != y2:
        data[sy][sx] = "|"
    elif (x1 < sx or x2 < sx) and (y1 < sy or y2 < sy):
        data[sy][sx] = "J"
    elif (x1 > sx or x2 > sx) and (y1 < sy or y2 < sy):
        data[sy][sx] = "L"
    elif (x1 < sx or x2 < sx) and (y1 > sy or y2 > sy):
        data[sy][sx] = "7"
    elif (x1 > sx or x2 > sx) and (y1 > sy or y2 > sy):
        data[sy][sx] = "F"
    else:
        raise Exception(
            f"Could not determine start pipe: {x1} {y1} | {x2} {y2} | {sx} {sy}"
        )

    def move_to_next(x, y):
        possibilities = {
            "-": [(x - 1, y), (x + 1, y)],
            "|": [(x, y - 1), (x, y + 1)],
            "7": [(x - 1, y), (x, y + 1)],
            "F": [(x + 1, y), (x, y + 1)],
            "L": [(x, y - 1), (x + 1, y)],
            "J": [(x - 1, y), (x, y - 1)],
            "S": [],
        }
        for dx, dy in possibilities[at(x, y)]:
            if not is_visited(dx, dy):
                return dx, dy
        raise Exception(f"No way out! {x}, {y}")

    distance = 1
    while x1 != x2 or y1 != y2:
        distance += 1
        x1, y1 = move_to_next(x1, y1)
        x2, y2 = move_to_next(x2, y2)
        if x1 == x2 and y1 == y2:
            visited.add((x1, y1))
            break
        visited.add((x1, y1))
        visited.add((x2, y2))

    visited_data = [
        ["v" if (x, y) in visited else "." for x in range(w)] for y in range(h)
    ]
    for line in visited_data:
        print("".join(line))

    inout = [["." for _ in range(w)] for _ in range(h)]

    for x in range(w):
        for y in range(h):
            if data[y][x] != ".":
                if (x, y) not in visited:
                    data[y][x] = "."

    c = 0
    for x in range(w):
        for y in range(h):
            t = data[y][x]
            if t == ".":
                crossings = 0
                pipe_start = None
                xx = x
                while xx > 0:
                    t = data[y][xx]

                    if t == "|":
                        if pipe_start:
                            raise Exception(
                                f"Uhm, pipe interrupted {xx} {y}. start x = {x}"
                            )
                        crossings += 1
                    elif t == "-":
                        if not pipe_start:
                            raise Exception(
                                f"Horz while not in pipe! {xx} {y}. start x = {x}"
                            )
                            pass
                    elif t == "F":
                        if pipe_start == "J":
                            crossings += 1
                        pipe_start = None
                    elif t == "L":
                        if pipe_start == "7":
                            crossings += 1
                        pipe_start = None
                    elif t == "7" or t == "J":
                        pipe_start = t
                    elif t != "." and t != "x":
                        raise Exception(
                            f"Unexpected pipe {t} at {xx} {y}. start x = {x}"
                        )

                    xx -= 1

                if crossings % 2 == 1:
                    inout[y][x] = "I"
                    c += 1
                else:
                    inout[y][x] = "O"

    print()
    for line in data:
        print("".join(line))
    print()
    for line in inout:
        print("".join(line))

    return c


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
