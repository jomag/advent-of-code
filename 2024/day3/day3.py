# I guessed that complexity would blow up for the second part, so I
# implemented a simple state machine for part 1.
# In retrospect, it could have been quite easily solved using regex.


def solve(data, always_do=True):
    data = " ".join(data)
    state = 0
    op1 = 0
    op2 = 0
    ops = []
    do = True

    for c in data:
        match state:
            case 0 if c == "m":
                state = 1
                op1 = 0
                op2 = 0
            case 0 if c == "d":
                state = 100
            case 1 if c == "u":
                state = 2
            case 2 if c == "l":
                state = 3
            case 3 if c == "(":
                state = 4
            case 4 if c.isnumeric():
                state = 5
                op1 = int(c)
            case 5 | 6 if c.isnumeric():
                op1 = op1 * 10 + int(c)
                state += 1
            case 5 | 6 if c == ",":
                state = 8
            case 7 if c == ",":
                state = 8
            case 8 if c.isnumeric():
                state = 9
                op2 = int(c)
            case 9 | 10 if c.isnumeric():
                op2 = op2 * 10 + int(c)
                state += 1
            case 9 | 10 if c == ")":
                if do or always_do:
                    ops.append((op1, op2))
                state = 0
            case 11 if c == ")":
                if do or always_do:
                    ops.append((op1, op2))
                state = 0
            case 100 if c == "o":
                state = 101
            case 101 if c == "(":
                state = 110
            case 101 if c == "n":
                state = 120
            case 110 if c == ")":
                do = True
                state = 0
            case 120 if c == "'":
                state = 121
            case 121 if c == "t":
                state = 122
            case 122 if c == "(":
                state = 123
            case 123 if c == ")":
                do = False
                state = 0
            case _:
                state = 0

    return sum([op[0] * op[1] for op in ops])


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

example1 = ["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]
example2 = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]

print(f"Part 1 with example data: {solve(example1)}")
print(f"Part 1 with real input: {solve(lines)}")
print(f"Part 2 with example data: {solve(example2, always_do=False)}")
print(f"Part 2 with real input: {solve(lines, always_do=False)}")
