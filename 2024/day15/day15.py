import time


def parse(data):
    moves, robot, boxes, walls = None, None, set(), set()

    for y, line in enumerate(data):
        if data[y] == "":
            moves = "".join(data[y + 1 :])
            break

        for x, c in enumerate(line):
            if c == "#":
                walls.add((x, y))
            if c == "@":
                robot = (x, y)
            if c == "O":
                boxes.add((x, y))

    return walls, boxes, robot, moves


def part1(data, verbose=False):
    walls, boxes, robot, moves = data
    walls = walls.copy()
    boxes = boxes.copy()
    rx, ry = robot

    def print_state():
        w = max([w[0] for w in walls]) + 1
        h = max([w[1] for w in walls]) + 1
        for y in range(h):
            s = ""
            for x in range(w):
                if (x, y) in walls:
                    s += "#"
                elif (x, y) in boxes:
                    s += "O"
                elif (x, y) == (rx, ry):
                    s += "@"
                else:
                    s += "."
            print(s)
        print()

    if verbose:
        print(f"Initial state: {rx},{ry}")
        print_state()

    def push_box(bx, by, dx, dy):
        nx, ny = bx + dx, by + dy
        if (nx, ny) in walls:
            return False
        if (nx, ny) in boxes:
            if not push_box(nx, ny, dx, dy):
                return False
        boxes.remove((bx, by))
        boxes.add((nx, ny))
        return True

    def move(dx, dy):
        nx, ny = rx + dx, ry + dy
        if (nx, ny) in walls:
            return rx, ry
        elif (nx, ny) in boxes:
            if not push_box(nx, ny, dx, dy):
                return rx, ry
        return nx, ny

    dirs = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
    for m in moves:
        rx, ry = move(*dirs[m])
        if verbose:
            print(f"Move {m}")
            print_state()
            print()
            # input()

    if verbose:
        print("final state")
        print_state()

    return sum([o[1] * 100 + o[0] for o in boxes])


def part2(data, verbose=False):
    walls, boxes, robot, moves = data
    walls = walls.copy()
    boxes = boxes.copy()
    rx, ry = robot

    # Double the width
    w1 = set([(w[0] * 2, w[1]) for w in walls])
    w2 = set([(w[0] * 2 + 1, w[1]) for w in walls])
    walls = set([*w1, *w2])
    boxes = set([(b[0] * 2, b[1]) for b in boxes])
    rx *= 2

    def print_state():
        w = max([w[0] for w in walls]) + 1
        h = max([w[1] for w in walls]) + 1
        for y in range(h):
            s = ""
            for x in range(w):
                if (x, y) == (rx, ry):
                    s += "@"
                elif (x, y) in walls:
                    s += "#"
                elif (x, y) in boxes:
                    s += "["
                elif (x - 1, y) in boxes:
                    s += "]"
                else:
                    s += "."
            print(s)
        print()

    if verbose:
        print(f"Initial state: {rx},{ry}")
        print_state()

    def push_box(bx, by, dx, dy):
        nonlocal boxes

        # bx can be either the left or right side of the box
        # Adjust bx so it always point at the left side of the box
        if (bx, by) not in boxes and (bx - 1, by) in boxes:
            bx = bx - 1

        if dx == 1 and dy == 0:
            if (bx + 2, by) in walls:
                return False
            elif (bx + 2, by) in boxes and not push_box(bx + 2, by, dx, dy):
                return False

        elif dx == -1 and dy == 0:
            if (bx - 1, by) in walls:
                return False
            elif (bx - 2, by) in boxes and not push_box(bx - 2, by, dx, dy):
                return False

        elif dx == 0 and dy == -1:
            if (bx, by - 1) in walls or (bx + 1, by - 1) in walls:
                return False
            elif (bx, by - 1) in boxes and not push_box(bx, by - 1, dx, dy):
                return False

            old_boxes = boxes.copy()
            if (bx - 1, by - 1) in boxes and not push_box(bx - 1, by - 1, dx, dy):
                return False
            if (bx + 1, by - 1) in boxes and not push_box(bx + 1, by - 1, dx, dy):
                boxes = old_boxes
                return False

        elif dx == 0 and dy == 1:
            if (bx, by + 1) in walls or (bx + 1, by + 1) in walls:
                return False
            elif (bx, by + 1) in boxes and not push_box(bx, by + 1, dx, dy):
                return False

            old_boxes = boxes.copy()
            if (bx - 1, by + 1) in boxes and not push_box(bx - 1, by + 1, dx, dy):
                return False
            if (bx + 1, by + 1) in boxes and not push_box(bx + 1, by + 1, dx, dy):
                boxes = old_boxes
                return False

        boxes.remove((bx, by))
        boxes.add((bx + dx, by + dy))
        return True

    def move(dx, dy):
        nx, ny = rx + dx, ry + dy
        if (nx, ny) in walls:
            return rx, ry
        elif (nx, ny) in boxes or (nx - 1, ny) in boxes:
            if push_box(nx, ny, dx, dy):
                return nx, ny
            else:
                return rx, ry
        else:
            return nx, ny

    dirs = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
    for m in moves:
        rx, ry = move(*dirs[m])
        if verbose:
            print(f"Move {m}. {rx},{ry}")
            print_state()
            print()
            input()

    if verbose:
        print("final state")
        print_state()

    return sum([o[1] * 100 + o[0] for o in boxes])


def run(label, f, data, verbose=False):
    start = time.perf_counter()
    result = f(data, verbose=verbose)
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

run("Part 1 with example data", part1, example, verbose=False)
run("Part 1 with real input", part1, lines, verbose=False)
run("Part 2 with example data", part2, example, verbose=False)
run("Part 2 with real input", part2, lines, verbose=False)
