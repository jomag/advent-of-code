from functools import cache


def parse(data):
    return list(map(int, data[0].split()))


def part1(data, verbose=False):
    def iter(stones):
        sn = []
        for s in stones:
            if s == 0:
                sn.append(1)
            else:
                t = str(s)
                if len(t) % 2 == 0:
                    a, b = t[len(t) // 2 :], t[: len(t) // 2]
                    sn.append(int(a))
                    sn.append(int(b))
                else:
                    sn.append(s * 2024)
        return sn

    if verbose:
        print("Initial")
        print(data)

    for n in range(25):
        data = iter(data)
        if verbose and n < 7:
            print(f"After {n+1} blink")
            print(data, f"({len(data)})\n")

    return len(data)


def part2(data):
    @cache
    def iterations_until_split(s):
        if s == 0:
            s = 1
            n = 1
        else:
            n = 0

        while len(str(s)) % 2 != 0:
            s = s * 2024
            n += 1

        t = str(s)
        a, b = t[len(t) // 2 :], t[: len(t) // 2]
        return (n + 1, int(a), int(b))

    @cache
    def eval_stone(s, n):
        m, left, right = iterations_until_split(s)
        if m > n:
            return 1
        else:
            return eval_stone(left, n - m) + eval_stone(right, n - m)

    return sum(eval_stone(s, 75) for s in data)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input:   {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input:   {part2(lines)}")
