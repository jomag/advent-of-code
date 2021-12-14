from collections import defaultdict


def parse(data):
    template = data[0]
    rules = [r.split(" -> ") for r in data[2:]]
    rules = {r[0]: r[1] for r in rules}
    return template, rules


def naive(data, verbose=False, steps=10):
    tpl, rules = parse(data)

    for step in range(steps):
        nt = ""
        for i in range(len(tpl) - 1):
            pair = tpl[i : i + 2]
            if pair in rules:
                nt += pair[0] + rules[pair]
            else:
                nt += pair[0]
        tpl = nt + tpl[-1]

        if verbose:
            print(f"Step {step +1}: {len(tpl)}")
            if len(tpl) < 30:
                print(f"  {tpl}")

    cnt = {c: tpl.count(c) for c in set(c for c in tpl)}
    return max(cnt.values()) - min(cnt.values())


def solve(data, verbose=False, steps=40):
    tpl, rules = parse(data)
    pairs = {}

    for i in range(len(tpl) - 1):
        pair = tpl[i : i + 2]
        try:
            pairs[pair] += 1
        except KeyError:
            pairs[pair] = 1

    char_count = defaultdict(lambda: 0)
    for c in tpl:
        char_count[c] += 1

    for _ in range(steps):
        np = {}
        for pair, cnt in pairs.items():
            # Assumption: there is a rule for every pair
            p1 = pair[0] + rules[pair]
            p2 = rules[pair] + pair[1]

            try:
                np[p1] += cnt
            except KeyError:
                np[p1] = cnt

            try:
                np[p2] += cnt
            except KeyError:
                np[p2] = cnt

            char_count[rules[pair]] += cnt

        pairs = np

    most = max(char_count.values())
    least = min(char_count.values())
    return most - least


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {naive(example, verbose=False, steps=10)}")
print(f"Part 1 with real input: {naive(lines, steps=10)}")
print(f"Part 2 with example data: {solve(example, verbose=True, steps=40)}")
print(f"Part 2 with real input: {solve(lines,steps=40)}")
