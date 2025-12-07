import time

def part1(data, verbose=False):
    nums = []
    for row in data[:-1]:
        nums.append([s for s in row.split(" ") if s != ""])
    ops = [s for s in data[-1].split(" ") if s != ""]

    tot = 0
    for n in range(len(ops)):
        op = ops[n]
        a = int(nums[0][n])
        for row in nums[1:]:
            if op == "*":
                a = a * int(row[n])
            if op == "+":
                a = a + int(row[n])
        tot = tot + a
    return tot

def part2(rows, verbose=False):
    ops = rows[-1]
    rows = rows[:-1]

    tot = 0
    for (n, op) in enumerate(ops):
        if op == " ":
            continue

        dig = n
        val = 0
        done = False
        colval = None

        while not done:
            done = True
            val = 0
            for row in rows:
                if len(row) > dig:
                    x = row[dig]
                else:
                    x = " "
                if x == " ":
                    pass
                else:
                    x = int(x)
                    val = val * 10 + x
                    done = False

            if not done:
                if op == "+":
                    if colval is None:
                        colval = val
                    else:
                        colval = colval + val
                else:
                    if colval is None:
                        colval = val
                    else:
                        colval = colval * val
            dig += 1

        tot = tot + colval

    return tot


def run(label, f):
    start = time.perf_counter()
    result = f()
    elapsed = time.perf_counter() - start
    if elapsed > 2:
        elapsed = f"{elapsed:.3f}s"
    else:
        elapsed = f"{elapsed*1000:.1f}ms"
    print(f"{label}: {result} ({elapsed})")


with open("input.txt") as f:
    lines = [ln.replace("\n", "") for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.replace("\n", "") for ln in f.readlines()]

run("Part 1 with example data", lambda: part1(example, verbose=False))
run("Part 1 with real input", lambda: part1(lines, verbose=False))
run("Part 2 with example data", lambda: part2(example, verbose=False))
run("Part 2 with real input", lambda: part2(lines, verbose=False))
