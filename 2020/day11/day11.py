import sys


def adjacent(board, x, y, dist=None):
    def look(nx, ny, dx, dy, dist=None):
        nx, ny = nx + dx, ny + dy
        while dist != 0 and nx >= 0 and nx < w and ny >= 0 and ny < h:
            if board[ny][nx] != ".":
                return board[ny][nx]
            nx, ny = nx + dx, ny + dy
            if dist is not None:
                dist -= 1

    h, w = len(board), len(board[0])
    return [
        look(x, y, -1, -1, dist),
        look(x, y, 0, -1, dist),
        look(x, y, 1, -1, dist),
        look(x, y, -1, 0, dist),
        look(x, y, 1, 0, dist),
        look(x, y, -1, 1, dist),
        look(x, y, 0, 1, dist),
        look(x, y, 1, 1, dist),
    ]


def step(board, limit, dist):
    def calc(x, y):
        nonlocal ch
        cur = board[y][x]
        if cur == ".":
            return "."
        adj = adjacent(board, x, y, dist)

        if cur == "L" and adj.count("#") == 0:
            ch += 1
            return "#"
        elif cur == "#" and adj.count("#") >= limit:
            ch += 1
            return "L"
        else:
            return cur

    ch = 0
    h = len(board)
    w = len(board[0])
    return [[calc(x, y) for x in range(w)] for y in range(h)], ch


def seated(board):
    return sum(row.count("#") for row in board)


def format_board(board):
    return "\n".join(["".join(row) for row in board])


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    initial = [[c for c in line.strip()] for line in f.readlines()]

r = 1
b, ch = step(initial, 4, 1)
while ch > 0:
    if filename != "input":
        print(f"\nRound {r}:")
        print(format_board(b))
    b, ch = step(b, 4, 1)
    r += 1

print(f"Part 1: Seated after {r} rounds: {seated(b)}")

r = 1
b, ch = step(initial, 5, None)
while ch > 0:
    if filename != "input":
        print(f"\nRound {r}:")
        print(format_board(b))
    b, ch = step(b, 5, None)
    r += 1

print(f"Part 2: Seated after {r} rounds: {seated(b)}")
