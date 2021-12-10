import collections

pairs = {
    "(": ")",
    "[": "]",
    "<": ">",
    "{": "}",
}

opening = pairs.keys()


def part1(data, verbose=False):
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0

    for line in data:
        q = collections.deque()

        for tok in line:
            if tok in opening:
                q.append(tok)
            else:
                prev = q.pop()
                if pairs[prev] != tok:
                    if verbose:
                        print(f"{line}: Expected closing {prev}, got {tok}")
                    score += scores[tok]

    return score


def part2(data, verbose=False):
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    score = []

    for line in data:
        q = collections.deque()
        for tok in line:
            if tok in opening:
                q.append(tok)
            else:
                prev = q.pop()
                if pairs[prev] != tok:
                    break
        else:
            if len(q) > 0:
                s = 0
                while q:
                    s = s * 5 + scores[q.pop()]
                score.append(s)

    return sorted(score)[len(score) // 2]


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]


with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
