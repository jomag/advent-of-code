class Die:
    def __init__(self):
        self._value = 0
        self.rolls = 0

    def roll(self):
        self._value = (self._value + 1) % 100
        self.rolls += 1
        return self._value


def part1(plr1, plr2, win, verbose=False):
    score1, score2 = 0, 0
    die = Die()

    while True:
        rolls = []
        for _ in range(3):
            roll = die.roll()
            rolls.append(str(roll))
            plr1 = (plr1 - 1 + roll) % 10 + 1
        score1 += plr1

        if verbose:
            print(f"Player 1: {'+'.join(rolls)} -> {plr1}. Total: {score1}.")

        if score1 >= win:
            break

        rolls = []
        for _ in range(3):
            roll = die.roll()
            rolls.append(str(roll))
            plr2 = (plr2 - 1 + roll) % 10 + 1
        score2 += plr2

        if verbose:
            print(f"Player 2: {'+'.join(rolls)} -> {plr2}. Total: {score2}.")

        if score2 >= win:
            break

    return die.rolls * min(score1, score2)


def part2(plr1, plr2, win, verbose=False):
    plr1 = (plr1 - 1) % 10
    plr2 = (plr2 - 1) % 10
    wins1 = 0
    wins2 = 0

    universes = [
        [[[0 for _ in range(win)] for _ in range(win)] for _ in range(10)]
        for _ in range(10)
    ]

    universes[plr1][plr2][0][0] = 1

    # Rough estimate: every player gains at least 1 point every turn
    # so at worst it takes 21 turns to finish all rounds. It stabilizes
    # much faster than that though.
    for _ in range(21 // 2):
        ucopy = [
            [[[0 for _ in range(win)] for _ in range(win)] for _ in range(10)]
            for _ in range(10)
        ]

        for pos1 in range(10):
            for pos2 in range(10):
                for pt1 in range(win):
                    for pt2 in range(win):
                        next_positions = {
                            (pos1 + 3) % 10: 1,
                            (pos1 + 4) % 10: 3,
                            (pos1 + 5) % 10: 6,
                            (pos1 + 6) % 10: 7,
                            (pos1 + 7) % 10: 6,
                            (pos1 + 8) % 10: 3,
                            (pos1 + 9) % 10: 1,
                        }
                        cnt = universes[pos1][pos2][pt1][pt2]
                        for new_pos, mul in next_positions.items():
                            new_pt = pt1 + new_pos + 1
                            if new_pt >= win:
                                wins1 += cnt * mul
                            else:
                                ucopy[new_pos][pos2][new_pt][pt2] += cnt * mul
        universes = ucopy

        ucopy = [
            [[[0 for _ in range(win)] for _ in range(win)] for _ in range(10)]
            for _ in range(10)
        ]

        for pos1 in range(10):
            for pos2 in range(10):
                for pt1 in range(win):
                    for pt2 in range(win):
                        next_positions = {
                            (pos2 + 3) % 10: 1,
                            (pos2 + 4) % 10: 3,
                            (pos2 + 5) % 10: 6,
                            (pos2 + 6) % 10: 7,
                            (pos2 + 7) % 10: 6,
                            (pos2 + 8) % 10: 3,
                            (pos2 + 9) % 10: 1,
                        }
                        cnt = universes[pos1][pos2][pt1][pt2]
                        for new_pos, mul in next_positions.items():
                            new_pt = pt2 + new_pos + 1
                            if new_pt >= win:
                                wins2 += cnt * mul
                            else:
                                ucopy[pos1][new_pos][pt1][new_pt] += cnt * mul
        universes = ucopy

        if verbose:
            print(f"Wins: {wins1} vs {wins2}")

    return max(wins1, wins2)


print(f"Part 1 with example data: {part1(4, 8, 1000, verbose=False)}")
print(f"Part 1 with real input: {part1(5, 8, 1000)}")
print(f"Part 2 with example data: {part2(4, 8, 21, verbose=False)}")
print(f"Part 2 with real input: {part2(5, 8, 21)}")
