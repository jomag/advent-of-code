
WIN_SCORE = 6
DRAW_SCORE = 3


def part1(rounds, verbose=False):
    score = 0

    for r in rounds:
        if (r[0] + 1) % 3 == r[1]:
            score += WIN_SCORE
        elif r[0] == r[1]:
            score += DRAW_SCORE
        score += r[1] + 1

    return score


def part2(rounds, verbose=False):
    score = 0

    for r in rounds:
        if r[1] == 0:
            score += (r[0] - 1) % 3 + 1
        elif r[1] == 1:
            score += r[0] + 1 + DRAW_SCORE
        else:
            score += (r[0] + 1) % 3 + 1 + WIN_SCORE

    return score


with open("input.txt") as f:
    rounds = [ln.strip().split() for ln in f.readlines()]
    rounds = [(ord(r[0]) - ord('A'), ord(r[1]) - ord('X')) for r in rounds]

with open("example.txt") as f:
    example = [ln.strip().split() for ln in f.readlines()]
    example = [(ord(r[0]) - ord('A'), ord(r[1]) - ord('X')) for r in example]

print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(rounds)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(rounds)}")
