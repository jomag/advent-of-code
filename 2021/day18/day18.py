from math import floor, ceil


def parse(data):
    numbers = []

    for line in data:
        num = []
        for i in range(len(line)):
            if line[i] in ("[", "]"):
                num.append(line[i])
            elif line[i].isnumeric():
                num.append(int(line[i]))
            else:
                assert line[i] == ","
        numbers.append(num)

    return numbers


def sf_fmt(l):
    return " ".join(str(v) for v in l)


def sf_add(a, b):
    return sf_reduce(["[", *a, *b, "]"])


def sf_reduce(s):
    finished = False

    while not finished:
        finished = True

        # Explode ...
        i, depth = 0, 0
        while i < len(s):
            if s[i] == "[":
                depth = depth + 1
                if depth > 4:
                    finished = False
                    assert type(s[i + 1]) == int
                    assert type(s[i + 2]) == int
                    left = s[i + 1]
                    right = s[i + 2]

                    s = s[0:i] + [0] + s[i + 4 :]

                    j = i - 1
                    while j > 0:
                        if type(s[j]) is int:
                            s[j] += left
                            break
                        j -= 1

                    j = i + 1
                    while j < len(s):
                        if type(s[j]) is int:
                            s[j] += right
                            break
                        j += 1

                    i, depth = 0, 0
                    continue

            elif s[i] == "]":
                depth = depth - 1

            i += 1

        # Split ...
        i = 0
        while i < len(s):
            if type(s[i]) is int:
                if s[i] > 9:
                    finished = False
                    a, b = floor(s[i] / 2.0), ceil(s[i] / 2.0)
                    s = s[0:i] + ["[", a, b, "]"] + s[i + 1 :]
                    break
            i += 1

    return s


def sf_magnitude(n):
    i = 0

    def rec():
        nonlocal i

        assert n[i] == "["
        i += 1

        if type(n[i]) is int:
            left = n[i]
            i += 1
        else:
            left = rec()

        if type(n[i]) is int:
            right = n[i]
            i += 1
        else:
            right = rec()

        assert n[i] == "]"
        i += 1

        return left * 3 + right * 2

    return rec()


def part1(data, verbose=False):
    numbers = parse(data)
    total = numbers[0]

    for i in range(len(numbers) - 1):
        total = sf_reduce(sf_add(total, numbers[i + 1]))

    return sf_magnitude(total)


def part2(data, verbose=False):
    numbers = parse(data)
    highest = 0

    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j:
                highest = max(sf_magnitude(sf_add(numbers[i], numbers[j])), highest)

    return highest


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
