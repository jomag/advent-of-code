import time
from functools import cache
from itertools import permutations
from typing import Tuple

numeric_keypad = ("789", "456", "123", " 0A")
directional_keypad = (" ^A", "<v>")


@cache
def get_button_position(btn: str, keypad: Tuple[str, ...]):
    for i, row in enumerate(keypad):
        if btn in row:
            return row.index(btn), i
    raise Exception("Invalid button: " + btn)


@cache
def find_best_move(a: str, b: str, keypad: Tuple[str, ...], iter) -> int:
    if a == b:
        return 1

    def validate(x: int, y: int, instr: str):
        for c in instr:
            if keypad[y][x] == " ":
                return False
            if c == "<":
                x -= 1
            if c == ">":
                x += 1
            if c == "^":
                y -= 1
            if c == "v":
                y += 1
        if keypad[y][x] == " ":
            return False
        return True

    x1, y1 = get_button_position(a, keypad)
    x2, y2 = get_button_position(b, keypad)

    moves = ""
    if x2 < x1:
        moves += "<" * (x1 - x2)
    if x2 > x1:
        moves += ">" * (x2 - x1)
    if y2 < y1:
        moves += "^" * (y1 - y2)
    if y2 > y1:
        moves += "v" * (y2 - y1)

    # "moves" now contains one optimal path from x1,y1 to x2,y2,
    # from the perpective of the current "robot". If there are no
    # more robots after this one, we've found the lowest number
    # of presses to go from x1,y1 to x2,y2.
    if iter == 0:
        return len(moves) + 1

    # If there are more robots, we need to consider them in turn.
    # Create a list of all permutations of the path from x1,y1
    # to x2,y2 that do not pass the "invalid" position, and
    # then validate each of them with all robots that comes
    # after the current one.
    possibilities = set("".join(perm) + "A" for perm in permutations(moves))
    possibilities = set(filter(lambda i: validate(x1, y1, i), possibilities))

    result = None
    for p in possibilities:
        btn = "A"
        tot = 0
        for c in p:
            tot += find_best_move(btn, c, directional_keypad, iter - 1)
            btn = c
        if result is None or tot < result:
            result = tot

    if result is None:
        raise Exception("No valid result found!")
    if result == 0:
        raise Exception("Invalid result with 0 kepresses")
    return result


def solve(data, bots):
    def solve(code):
        a = "A"
        tot = 0
        for b in code:
            tot += find_best_move(a, b, numeric_keypad, bots)
            a = b
        return tot * int(code[:-1])

    return sum(solve(code) for code in data)


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

run("Part 1 with example data", lambda: solve(example, 2))
run("Part 1 with real input", lambda: solve(lines, 2))
run("Part 2 with example data", lambda: solve(example, 25))
run("Part 2 with real input", lambda: solve(lines, 25))
