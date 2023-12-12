from functools import cmp_to_key
from typing import List, Union

# Determine if `left` should be placed before `right`
# Returns:
# -1 if left should be before right
# +1 if right should be before left
# 0 if equal priority
def compare(left, right):
    LEFT_BEFORE_RIGHT = -1
    RIGHT_BEFORE_LEFT = +1
    SAME = 0

    if type(left) == int and type(right) == int:
        if left < right:
            return LEFT_BEFORE_RIGHT
        if left > right:
            return RIGHT_BEFORE_LEFT
        return SAME

    if type(left) == int:
        left = [left]
    if type(right) == int:
        right = [right]

    for n in range(len(left)):
        if n >= len(right):
            return RIGHT_BEFORE_LEFT

        cmp = compare(left[n], right[n])
        if cmp != SAME:
            return cmp

    if len(left) == len(right):
        return SAME

    return LEFT_BEFORE_RIGHT


def part1(data):
    return sum(n + 1 for n, pair in enumerate(data) if compare(*pair) <= 0)


def part2(data):
    v = [[2], [6]]
    for p in data:
        v.append(p[0])
        v.append(p[1])

    vs = sorted(v, key=cmp_to_key(compare))

    idx1 = 0
    idx2 = 0
    for n in range(len(vs)):
        if vs[n] == [2]:
            idx1 = n + 1
        if vs[n] == [6]:
            idx2 = n + 1

    return idx1 * idx2


def parse(lines):
    pairs = []
    a = None
    for n in range(len(lines)):
        if n % 3 == 0:
            a = lines[n]
        elif n % 3 == 1:
            pairs.append((a, lines[n]))

    def parse_list(tokens, i):
        assert tokens[i] == "["
        i += 1
        lst = []

        while i < len(tokens):
            t = tokens[i]
            if type(t) == int:
                lst.append(t)
            elif t == "[":
                cl, i = parse_list(tokens, i)
                lst.append(cl)
            elif t == "]":
                return lst, i
            i += 1

        raise Exception("out of data")

    def parse_line(line):
        # Tokenize
        n = 0
        tokens = []
        while n < len(line):
            c = line[n]
            n += 1
            if c.isnumeric():
                v = int(c)
                while line[n].isnumeric():
                    v = v * 10 + int(line[n])
                    n += 1
                tokens.append(v)
            elif c == "[" or c == "]":
                tokens.append(c)
            else:
                assert c == ","

        lst, _ = parse_list(tokens, 0)
        return lst

    pairs = [(parse_line(p[0]), parse_line(p[1])) for p in pairs]
    return pairs


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
