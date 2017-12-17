
def part1(data):
    data = list(data)
    ptr = 0
    steps = 0
    try:
        while True:
            j = data[ptr]
            data[ptr] += 1
            ptr = ptr + j
            steps += 1
    except IndexError:
        return steps, data


def part2(data):
    data = list(data)
    ptr = 0
    steps = 0
    try:
        while True:
            j = data[ptr]
            if j >= 3:
                data[ptr] -= 1
            else:
                data[ptr] += 1
            ptr = ptr + j
            steps += 1
    except IndexError:
        return steps, data


with open("day5.txt") as fp:
    data = [int(line) for line in fp.read().splitlines()]

n, new_data = part1([0, 3, 0, 1, -3])
assert n == 5
assert new_data == [2, 5, 0, 1, -2]

n, new_data = part2([0, 3, 0, 1, -3])
assert n == 10
assert new_data == [2, 3, 2, 3, -1]

print(part1(data)[0])
print(part2(data)[0])
