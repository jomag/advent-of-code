# Be prepared for some really messy code!
#
# At first I had a quite clean solution, but I missed one condition
# in the description that stated that the mirror line for part 2
# must not be the same as in part 1. The examples still worked,
# but not the input data.
#
# So I started messing with the code until I ended up with this
# mess, and then when I found my mistake I could not be bothered
# to return it to a clean state again. :)


def parse(data):
    patterns = []

    rows = []
    for line in data + [""]:
        if not line.strip() and len(rows) > 0:
            columns = []
            for i in range(len(rows[0])):
                col = [row[i] for row in rows]
                columns.append("".join(col))
            patterns.append({"rows": rows, "columns": columns})
            rows = []
        else:
            rows.append(line)

    return patterns


def part1(data, verbose=False):
    def find_reflection(p):
        for n in range(len(p) - 1):
            if p[n] == p[n + 1]:
                for i in range(len(p)):
                    if n - i >= 0 and n + 1 + i < len(p):
                        if p[n - i] != p[n + 1 + i]:
                            break
                else:
                    return n

    patterns = parse(data)
    tot = 0

    for n, p in enumerate(patterns):
        row = find_reflection(p["rows"])
        col = find_reflection(p["columns"])
        score = 0
        if row is not None:
            score += (row + 1) * 100
        if col is not None:
            score += col + 1
        print(f"Pattern {n}: Row: {row} Col: {col} Score: {score}")
        tot += score

    return tot


def part2(data, verbose=False):
    def has_smudge(a, b):
        diff = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                diff += 1
        return diff == 1

    def find_reflection_p1(p):
        for n in range(len(p) - 1):
            if p[n] == p[n + 1]:
                for i in range(len(p)):
                    if n - i >= 0 and n + 1 + i < len(p):
                        if p[n - i] != p[n + 1 + i]:
                            break
                else:
                    return n

    def find_reflection(p, smudge_detected):
        p1 = find_reflection_p1(p)

        for n in range(len(p) - 1):
            print(f"Test line {n}")
            smudge_detected_here = False
            if n == p1:
                continue

            a = p[n]
            b = p[n + 1]

            if not smudge_detected and not smudge_detected_here and has_smudge(a, b):
                print(f"OHH SMUDGE! {n}")
                # smudge_detected = True
                smudge_detected_here = True
                smudge_index = n + 1
                smudge_repl = a
                # p[n + 1] = a
                b = a

            if a == b:
                print(f"Mirror paired line found at {n}")
                for i in range(1, len(p)):
                    if n - i >= 0 and n + 1 + i < len(p):
                        a = p[n - i]
                        b = p[n + 1 + i]
                        if a != b:
                            if smudge_detected or smudge_detected_here:
                                print(
                                    f"Diff (i={i}, n={n}) on {n-i} / {n+1+i} ({a} vs {b}) | {p[n-i]} | {p[n+1+i]} and already samuidged"
                                )
                                break
                            elif has_smudge(a, b):
                                # smudge_detected = True
                                smudge_detected_here = True
                                smudge_index = n + 1 + i
                                smudge_repl = a
                                # p[n + 1 + i] = a
                                print("SMUDGE!")
                            else:
                                print("Nah!")
                                break
                else:
                    print("OK!!")
                    if smudge_detected_here:
                        print(f"SMUDGE INDEX: {smudge_index}. Repl: {smudge_repl}")
                        p[smudge_index] = smudge_repl
                    return n + 1, smudge_detected_here or smudge_detected
        return None, smudge_detected

    patterns = parse(data)
    tot = 0

    for n, p in enumerate(patterns):
        row, smudge_detected = find_reflection(p["rows"], False)
        if smudge_detected:
            print("Fixed:")
            for line in p["rows"]:
                print(line)

            rows = p["rows"]
            columns = []
            for i in range(len(rows[0])):
                col = [row[i] for row in rows]
                columns.append("".join(col))
            p["columns"] = columns

            print("Fixed columns:")
            for line in p["columns"]:
                print(line)

        col, _ = find_reflection(p["columns"], smudge_detected)
        score = 0

        if row is not None:
            score += row * 100
        elif col is not None:
            score += col
        else:
            raise Exception(f"WHOA NO MIKRROR LINE IN {n}")

        print(f"Pattern {n}: Row: {row} Col: {col} Score: {score}")
        tot += score

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with real input: {part2(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
