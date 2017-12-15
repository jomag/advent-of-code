
ex1 = """5 1 9 5
7 5 3
2 4 6 8"""

ex2 = """5 9 2 8
9 4 7 3
3 8 6 5"""

def part1(txt):
    data = [[int(x) for x in line.split()] for line in txt.splitlines()]
    return sum(max(line) - min(line) for line in data)

def part2(txt):
    data = [[int(x) for x in line.split()] for line in txt.splitlines()]

    def chk(line):
        s = 0
        for a in line:
            for b in line:
                if a != b and a % b == 0:
                    s += a // b
        return s

    return sum(chk(line) for line in data)

with open("day2.txt") as fp:
    data = fp.read()

print(part1(ex1))
print(part1(data))
print(part2(ex2))
print(part2(data))

