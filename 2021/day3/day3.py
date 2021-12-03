def most_common_at_position(data, n):
    bits = [line[n] for line in data]
    zeros = bits.count("0")
    ones = bits.count("1")
    if zeros > ones:
        return "0"
    elif zeros < ones:
        return "1"
    return None


def part1(data):
    gamma = "".join(str(most_common_at_position(data, n)) for n in range(len(data[0])))
    epsilon = gamma.replace("1", "x").replace("0", "1").replace("x", "0")
    epsilon = int(epsilon, 2)
    gamma = int(gamma, 2)
    return gamma * epsilon


def part2(data):
    oxy = ""
    co2 = ""
    oxy_data = data.copy()
    co2_data = data.copy()

    for b in range(len(data[0])):
        if len(oxy_data) > 1:
            most_common = most_common_at_position(oxy_data, b) or "1"
            oxy_data = [line for line in oxy_data if line[b] == most_common]
        if len(co2_data) > 1:
            most_common = most_common_at_position(co2_data, b) or "1"
            co2_data = [line for line in co2_data if line[b] != most_common]

    oxy = int(oxy_data[0], 2)
    co2 = int(co2_data[0], 2)
    return oxy * co2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
