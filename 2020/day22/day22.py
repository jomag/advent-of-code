import sys


def play(decks, part=1, game=1):
    verbose(f"\n=== Game {game} ===\n")
    played = set()
    r = 0

    while all([len(deck) > 0 for deck in decks]):
        r += 1
        verbose(f"-- Round {r} (Game {game}) --")
        winner = None

        for i, deck in enumerate(decks):
            verbose(f"Player {i+1}'s deck: {', '.join([str(c) for c in deck])}")
        for i, deck in enumerate(decks):
            verbose(f"Player {i+1} plays: {deck[0]}")

        if part == 2:
            s1 = ",".join([str(c) for c in decks[0]])
            s2 = ",".join([str(c) for c in decks[1]])
            s = f"{s1}|{s2}"
            if s in played:
                verbose(f"Deck {i+1} is already played!")
                return 0, decks
            played.add(s)

        # Hint: there's only one card of each value
        p1, p2 = decks[0].pop(0), decks[1].pop(0)

        if part == 2 and len(decks[0]) >= p1 and len(decks[1]) >= p2:
            verbose("Enter new game with decks: ", decks)
            deck1 = decks[0][:p1]
            deck2 = decks[1][:p2]
            winner = play([deck1, deck2], part, game + 1)[0]
        else:
            if p1 > p2:
                winner = 0
            else:
                winner = 1

        if winner == 0:
            decks[0].extend([p1, p2])
        else:
            decks[1].extend([p2, p1])

        verbose(f"Player {winner+1} wins round {r} of game {game}!")

    for i, deck in enumerate(decks):
        if len(deck) > 0:
            winner = i

    if game > 1:
        verbose(f"...anyway, back to game {game - 1} ({decks}) {winner}")

    return winner, decks


def score(deck):
    return sum(c * (i + 1) for i, c in enumerate(deck[::-1]))


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    content = f.read()
    content = content.split("\n\n")
    assert len(content) == 2
    assert content[0].startswith("Player")
    assert content[1].startswith("Player")
    decks = [[line for line in deck.split("\n")[1:]] for deck in content]
    decks = [[int(c) for c in deck] for deck in decks]

if filename == "input" or True:
    verbose = lambda *a: None
else:
    verbose = print

print(f"== Post-game results ==")
winner, res = play([deck[:] for deck in decks], part=1)
for i, deck in enumerate(res):
    print(f"Player {i+1}'s deck: {', '.join([str(c) for c in deck])}")
[print(f"\nPart 1: {score(deck)}\n") for deck in res if len(deck) != 0]

if filename != "input":
    input("Press enter to continue...")

print(f"== Post-game results ==")
winner, res = play([deck[:] for deck in decks], part=2)
for i, deck in enumerate(res):
    print(f"Player {i+1}'s deck: {', '.join([str(c) for c in deck])}")
[print(f"Part 2: {score(deck)}") for deck in res if len(deck) != 0]
