from math import ceil, floor
from operator import attrgetter


class Monkey:
    starting_items: list[int]
    op: list[str]
    divisible_by: int
    throw_if_true: int
    throw_if_false: int

    def __init__(self):
        self.inspection_count = 0

    def __repr__(self):
        return f"Monkey({self.starting_items})"


def parse(data: list[str]):
    monkeys = []
    m = None
    for d in [d.strip() for d in data]:
        if d.startswith("Monkey"):
            _, n = d.split()
            assert int(n[:-1]) == len(monkeys)
            m = Monkey()
        if d.startswith("Starting items:"):
            assert m is not None
            d.replace(",", "")
            items = d.replace(",", "").split()[2:]
            m.starting_items = [int(n) for n in items]
        if d.startswith("Operation:"):
            assert m is not None
            p = d.split()
            assert p[0] == "Operation:" and p[1] == "new" and p[2] == "="
            m.op = p[3:]
        if d.startswith("Test:"):
            assert m is not None
            p = d.split()
            assert p[0] == "Test:" and p[1] == "divisible" and p[2] == "by"
            m.divisible_by = int(p[3])
        if d.startswith("If"):
            assert m is not None
            p = d.split()
            assert p[2] == "throw" and p[3] == "to" and p[4] == "monkey"
            if p[1] == "true:":
                m.throw_if_true = int(p[5])
            elif p[1] == "false:":
                m.throw_if_false = int(p[5])
            else:
                raise Exception(f"Invalid input: {d}")
        if d == "":
            monkeys.append(m)
            m = None
    if m is not None:
        monkeys.append(m)
    return monkeys


def part1(data, verbose=False):
    monkeys = parse(data)

    for _ in range(20):
        for m in monkeys:
            items = m.starting_items
            m.starting_items = []
            for it in items:
                m.inspection_count += 1
                assert m.op[0] == "old"
                b = it if m.op[2] == "old" else int(m.op[2])
                if m.op[1] == "+":
                    wl = it + b
                elif m.op[1] == "*":
                    wl = it * b
                else:
                    raise Exception(f"Unknown operation: f{m.op[1]}")
                wl = wl // 3
                if wl % m.divisible_by == 0:
                    monkeys[m.throw_if_true].starting_items.append(wl)
                else:
                    monkeys[m.throw_if_false].starting_items.append(wl)

    monkeys.sort(key=attrgetter("inspection_count"), reverse=True)
    return monkeys[0].inspection_count * monkeys[1].inspection_count


def part2(data, verbose=False):
    monkeys = parse(data)

    k = 1
    for m in monkeys:
        k = k * m.divisible_by

    for r in range(10_000):
        for m in monkeys:
            items = m.starting_items
            m.starting_items = []
            for it in items:
                m.inspection_count += 1
                assert m.op[0] == "old"
                b = it if m.op[2] == "old" else int(m.op[2])
                if m.op[1] == "+":
                    wl = it + b
                elif m.op[1] == "*":
                    wl = it * b
                else:
                    raise Exception(f"Unknown operation: f{m.op[1]}")
                wl = wl % k
                if wl % m.divisible_by == 0:
                    monkeys[m.throw_if_true].starting_items.append(wl)
                else:
                    monkeys[m.throw_if_false].starting_items.append(wl)

        if verbose and r + 1 in [1, 20, 1000, 2000, 3000, 4000, 10_000]:
            print(f"== After round {r+1} ==")
            for n in range(len(monkeys)):
                m = monkeys[n]
                print(f"Monkey {n} inspected items {m.inspection_count} times.")

    monkeys.sort(key=attrgetter("inspection_count"), reverse=True)
    return monkeys[0].inspection_count * monkeys[1].inspection_count


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, verbose=False)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=False)}")
print(f"Part 2 with real input: {part2(lines)}")
