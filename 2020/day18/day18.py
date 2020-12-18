import sys


def tokenize(line):
    t = []
    for c in line:
        if c.isnumeric():
            t.append(int(c))
        elif c in ["+", "-", "*", "/", "(", ")"]:
            t.append(c)
        elif c == " ":
            pass
        else:
            raise Exception(f"Invalid token: {c}")
    return t


def to_postfix(tokens, precedence):
    postfix = []
    stack = []

    for t in tokens:
        if type(t) is int:
            postfix.append(t)
        elif t == ")":
            while stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        else:
            while (
                len(stack) > 0
                and stack[-1] != "("
                and precedence[stack[-1]] >= precedence[t]
            ):
                postfix.append(stack.pop())
            stack.append(t)

    while len(stack) > 0:
        postfix.append(stack.pop())

    return postfix


def evaluate(postfix):
    stack = []
    for t in postfix:
        if type(t) is int:
            stack.append(t)
        elif t == "+":
            stack.append(stack.pop() + stack.pop())
        elif t == "-":
            stack.append(stack.pop() - stack.pop())
        elif t == "*":
            stack.append(stack.pop() * stack.pop())
        elif t == "/":
            stack.append(stack.pop() / stack.pop())
        else:
            raise Exception(f"Invalid token: {t}")
    return stack[-1]


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]

tokenized = [tokenize(line) for line in lines]

precedence = {"+": 10, "-": 10, "*": 10, "/": 10, "(": 100, ")": 100}
postfix = [to_postfix(infix, precedence) for infix in tokenized]
part1 = sum(evaluate(expr) for expr in postfix)
print(f"Part 1: {part1}")

precedence = {"+": 20, "-": 20, "*": 10, "/": 10, "(": 100, ")": 100}
postfix = [to_postfix(infix, precedence) for infix in tokenized]
part2 = sum(evaluate(expr) for expr in postfix)
print(f"Part 2: {part2}")
