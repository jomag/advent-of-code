def parse(data):
    w = 0
    h = 0

    def parse_one(line):
        nonlocal w, h
        parts = line.split(" ")
        x1, y1 = parts[0].split(",")
        x1, y1 = int(x1), int(y1)
        x2, y2 = parts[2].split(",")
        x2, y2 = int(x2), int(y2)
        w = max(w, x1, x2)
        h = max(h, y1, y2)
        return Line(x1, y1, x2, y2)

    return [parse_one(line) for line in data], w + 1, h + 1


class Line:
    x1: int
    y1: int
    x2: int
    y2: int

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def left(self):
        return min(self.x1, self.x2)

    @property
    def right(self):
        return max(self.x1, self.x2)

    @property
    def top(self):
        return min(self.y1, self.y2)

    @property
    def bottom(self):
        return max(self.y1, self.y2)

    def swap(self):
        return Line(self.x2, self.y2, self.x1, self.y1)


def print_board(b, w, h):
    char = lambda c: "." if c == 0 else str(c)
    rows = ["".join([char(b[y * w + x]) for x in range(w)]) for y in range(h)]
    print("\n".join(rows))


def draw_line(brd, ln, width):
    if ln.x1 == ln.x2:
        for y in range(ln.top, ln.bottom + 1):
            brd[y * width + ln.x1] += 1
    elif ln.y1 == ln.y2:
        for x in range(ln.left, ln.right + 1):
            brd[ln.y1 * width + x] += 1
    else:
        if ln.y2 < ln.y1:
            ln = ln.swap()
        dx = 1 if ln.x1 < ln.x2 else -1
        for y in range(ln.top, ln.bottom + 1):
            brd[y * width + ln.x1 + (y - ln.top) * dx] += 1


def solve(data, part: int):
    lines, width, height = parse(data)
    board = [0 for n in range(width * height)]

    if part == 1:
        lines = [l for l in lines if l.x1 == l.x2 or l.y1 == l.y2]

    for ln in lines:
        draw_line(board, ln, width)

    if width < 50:
        print_board(board, width, height)

    return len([b for b in board if b > 1])


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {solve(example,part=1)}")
print(f"Part 1 with real input: {solve(lines, part=1)}")
print(f"Part 2 with example data: {solve(example, part=2)}")
print(f"Part 2 with real input: {solve(lines,part=2)}")
