def part1(data: list[str]):
    x, y = 0, 0

    for op in data:
        d, n = op.split(" ")
        n = int(n)
        match d:
            case "forward":
                x += n
            case "up":
                y -= n
            case "down":
                y += n

    return x * y


def part2(data: list[str]):
    x, y, aim = 0, 0, 0

    for op in data:
        d, n = op.split(" ")
        n = int(n)
        match d:
            case "forward":
                x += n
                y += n * aim
            case "up":
                aim -= n
            case "down":
                aim += n

    return x * y


example = [
    "forward 5",
    "down 5",
    "forward 8",
    "up 3",
    "down 8",
    "forward 2",
]

with open("input") as f:
    lines = f.readlines()

print(f"Part 1, example: {part1(example)}")
print(f"Part 2, example: {part2(example)}")
print(f"Part 1: {part1(lines)}")
print(f"Part 2: {part2(lines)}")
