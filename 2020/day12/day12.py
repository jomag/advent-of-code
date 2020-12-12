import sys
from math import cos, sin, radians


def part1(prg):
    x, y, d = 0, 0, "e"
    for op in prg:
        m, v = op[0], op[1]
        if m == "f":
            m = d
        if m == "r":
            transl = {"e": "s", "s": "w", "w": "n", "n": "e"}
            for _ in range(v // 90):
                d = transl[d]
        if m == "l":
            transl = {"e": "n", "n": "w", "w": "s", "s": "e"}
            for _ in range(v // 90):
                d = transl[d]
        if m == "n":
            y -= v
        if m == "s":
            y += v
        if m == "e":
            x += v
        if m == "w":
            x -= v
    return x, y


def part2(prg):
    x, y, d, wx, wy = 0, 0, "e", 10, 1
    for op in prg:
        m, v = op[0], op[1]
        if m == "f":
            x += wx * v
            y += wy * v
        if m == "r":
            r = radians(-v)
            wx, wy = round(cos(r) * wx - sin(r) * wy), round(sin(r) * wx + cos(r) * wy)
        if m == "l":
            r = radians(+v)
            wx, wy = round(cos(r) * wx - sin(r) * wy), round(sin(r) * wx + cos(r) * wy)
        if m == "n":
            wy += v
        if m == "s":
            wy -= v
        if m == "e":
            wx += v
        if m == "w":
            wx -= v
    return x, y


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    prg = [(line[0].lower(), int(line[1:])) for line in f.readlines()]

x, y = part1(prg)
print(f"Part 1: abs({x}) + abs({y}) = {abs(x)+abs(y)}")

x, y = part2(prg)
print(f"Part 2: abs({x}) + abs({y}) = {abs(x)+abs(y)}")
