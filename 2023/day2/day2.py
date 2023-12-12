def parse(data):
    games = {}
    for line in data:
        a, b = line.split(":")
        game_id = int(a[4:])
        games[game_id] = []

        rounds = b.split(";")
        for r in rounds:
            round = {}
            for x in r.split(","):
                n, color = x.split()
                round[color] = int(n)
            games[game_id].append(round)

    return games


def part1(data, verbose=False):
    red = 12
    green = 13
    blue = 14
    id_sum = 0

    games = parse(data)
    for game, rounds in games.items():
        print(f"Game {game}: rounds = {rounds}")
        for round in rounds:
            if "red" in round and round["red"] > red:
                break
            if "green" in round and round["green"] > green:
                break
            if "blue" in round and round["blue"] > blue:
                break
        else:
            id_sum += game

    return id_sum


def part2(data, verbose=False):
    power = 0

    games = parse(data)
    for game, rounds in games.items():
        red = 0
        green = 0
        blue = 0
        print(f"Game {game}: rounds = {rounds}")
        for round in rounds:
            if "red" in round:
                red = max(red, round["red"])
            if "green" in round:
                green = max(green, round["green"])
            if "blue" in round:
                blue = max(blue, round["blue"])
        print(f"red={red} green={green} blue={blue}")
        power = power + red * green * blue

    return power


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
