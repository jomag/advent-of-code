from typing import Tuple


class Board:
    numbers = []
    marked = []

    def __init__(self, data: list[str]):
        self.numbers = [[int(n) for n in line.split(" ") if n] for line in data]
        self.marked = [[False for line in range(5)] for row in range(5)]

    def mark(self, num):
        for y in range(5):
            for x in range(5):
                if self.numbers[y][x] == num:
                    return self.mark_at(x, y)

    def mark_at(self, x, y):
        if not self.marked[y][x]:
            self.marked[y][x] = True
            return self.check_at(x, y)
        return False

    def check_at(self, x, y):
        if all(self.marked[y]):
            return True
        if all([self.marked[i][x] for i in range(5)]):
            return True
        return False

    def __str__(self):
        tot = ""
        for y in range(5):
            for x in range(5):
                if self.marked[y][x]:
                    tot = tot + "(%2d)  " % self.numbers[y][x]
                else:
                    tot = tot + " %2d   " % self.numbers[y][x]
            tot = tot + "\n"
        return tot

    def sum_of_unmarked(self):
        return sum(
            self.numbers[y][x]
            for x in range(5)
            for y in range(5)
            if not self.marked[y][x]
        )


def parse(inp: list[str]) -> Tuple[list[int], list[Board]]:
    draws = [int(n) for n in inp[0].split(",")]
    boards = [inp[i + 2 : i + 2 + 5] for i in range(0, len(inp) - 2, 6)]
    boards = [Board(board) for board in boards]
    return draws, boards


def part1(data):
    draws, boards = parse(data)

    for num in draws:
        for board in boards:
            if board.mark(num):
                return num * board.sum_of_unmarked()


def part2(data):
    draws, boards = parse(data)

    for num in draws:
        remaining_boards = []
        winner = None

        for board in boards:
            if board.mark(num):
                winner = board
            else:
                remaining_boards.append(board)

        if not remaining_boards:
            return num * winner.sum_of_unmarked()

        boards = remaining_boards


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
