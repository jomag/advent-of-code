# Note! I only solved part one for day 17, 2022

WIDTH = 7

HORZ = "horz"
VERT = "vert"
HOOK = "hook"
CROSS = "cross"
SQUARE = "square"

PIECES = {
    HORZ: ["####"],
    VERT: ["#", "#", "#", "#"],
    HOOK: ["..#", "..#", "###"],
    CROSS: [".#.", "###", ".#."],
    SQUARE: ["##", "##"],
}


class Playfield:
    def __init__(self):
        self.rows = {}

    def highest(self):
        if self.rows:
            return max(self.rows.keys()) + 1
        else:
            return 0

    def place(self, piece_type):
        self.piece_x = 2
        self.piece_y = self.highest() + 3
        self.piece_type = piece_type

    def print(self, verbose=True):
        piece = PIECES[self.piece_type]
        h = max(self.highest(), self.piece_y + len(piece)) + 2

        print(f"Piece: x={self.piece_x} y={self.piece_y} {self.piece_type}")

        for y in range(h, -1, -1):
            if y in self.rows:
                row = [c for c in self.rows[y]]
            else:
                row = ["."] * WIDTH

            if y >= self.piece_y and y < self.piece_y + len(piece):
                for x, c in enumerate(piece[self.piece_y - y + len(piece) - 1]):
                    if c == "#":
                        row[self.piece_x + x] = "@"

            print("".join(row))

    def push_left(self):
        px, py = self.piece_x - 1, self.piece_y
        if not self.test_collision(px, py):
            self.piece_x = px
        else:
            print("Collision!")

    def push_right(self):
        px, py = self.piece_x + 1, self.piece_y
        if not self.test_collision(px, py):
            self.piece_x = px
        else:
            print("Collision!")

    def push_down(self):
        px, py = self.piece_x, self.piece_y - 1
        if not self.test_collision(px, py):
            self.piece_y = py
            return True
        else:
            print("Collision!")
            return False

    def test_collision(self, x, y):
        piece = PIECES[self.piece_type]
        if x < 0:
            return True
        if x + len(piece[0]) > WIDTH:
            return True
        if y < 0:
            return True

        for dy in range(len(piece)):
            ry = y + len(piece) - dy - 1
            if ry in self.rows:
                for dx in range(len(piece[0])):
                    if piece[dy][dx] == "#":
                        if self.rows[ry][x + dx] == "#":
                            return True

        return False

    def rest_piece(self):
        piece = PIECES[self.piece_type]
        for dy in range(len(piece)):
            y = self.piece_y - dy + len(piece) - 1
            if y not in self.rows:
                self.rows[y] = ["."] * WIDTH
            for dx in range(len(piece[0])):
                if piece[dy][dx] == "#":
                    self.rows[y][self.piece_x + dx] = "#"


def part1(data, verbose=False):
    p = Playfield()

    piece_types = [HORZ, CROSS, HOOK, VERT, SQUARE]
    piece_idx = 0

    moves = data[0]
    move_idx = 0
    count = 0

    for n in range(2022):
        p.place(piece_types[piece_idx % 5])

        print("\nPlace new piece")
        # p.print()
        # input()

        piece_idx += 1
        while True:
            m = moves[move_idx % len(moves)]
            move_idx += 1

            if m == "<":
                # print("\nPush left:")
                p.push_left()
                # p.print()
            elif m == ">":
                # print("\nPush right:")
                p.push_right()
                # p.print()

            # input()

            if not p.push_down():
                # print("\nAt rest!")
                p.rest_piece()
                # p.print()
                break
            else:
                # print("\nMove down...")
                # p.print()
                pass

            # input()

    return max(p.rows.keys()) + 1


def part2(data, verbose=False):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
