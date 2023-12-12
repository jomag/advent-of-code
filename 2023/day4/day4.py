def part1(data, verbose=False):
    score = 0
    for line in data:
        card_no, rest = line.split(":")
        winning, numbers = rest.split("|")
        winning = [int(n) for n in winning.split()]
        numbers = [int(n) for n in numbers.split()]
        s = 0
        for n in numbers:
            if n in winning:
                s = s * 2 if s > 0 else 1
        score += s

    return score


class Card:
    def __init__(self, winning, numbers):
        self.winning = winning
        self.numbers = numbers
        self._score = None
        self.total_score = None
        self.card_wins = {}

    @property
    def score(self):
        if self._score is None:
            s = 0
            for n in self.numbers:
                if n in self.winning:
                    s += 1
            self._score = s
        return self._score

    def __repr__(self):
        return f"Card(winning={self.winning}, numbers={self.numbers}, total={self.total_score})"


def part2(data, verbose=False):
    cards = []
    for line in data:
        card_no, rest = line.split(":")
        winning, numbers = rest.split("|")
        winning = [int(n) for n in winning.split()]
        numbers = [int(n) for n in numbers.split()]
        cards.append(Card(winning, numbers))

    card_count = [1] * len(cards)

    def rec(n):
        card = cards[n]
        for m in range(card.score):
            idx = n + 1 + m
            if idx < len(cards):
                card_count[idx] += 1
                rec(idx)

    for n in range(len(cards)):
        print(f"Card {n}: {cards[n].score}")

    for n in range(len(cards)):
        print(f"Card {n}")
        rec(n)
        print(f"After evaluating {n}")
        print(f"Card {n}: {card_count}")

    print(card_count)

    # for n in reversed(range(len(cards))):
    #     won = [cards[n]]
    #     while len(won) > 0:
    #         new_wins = []
    #         for card in won:
    #             for m in range(card.score):
    #                 if n + m < len(cards):
    #                     new_wins.append(cards[n + m])
    #         won = new_wins

    #     print(f"Card {n}: score={card.score}")

    return sum(card_count)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
