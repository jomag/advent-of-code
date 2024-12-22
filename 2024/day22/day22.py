import time


def solve(initial: int):
    s = initial
    seq = ()
    prev = s % 10
    price_per_sequence = {}

    for _ in range(2000):
        s = ((s * 64) ^ s) % 16777216
        s = ((s >> 5) ^ s) % 16777216
        s = ((s * 2048) ^ s) % 16777216

        price = s % 10
        diff = price - prev
        seq = tuple(([*seq, diff])[-4:])
        prev = price

        if len(seq) == 4 and seq not in price_per_sequence:
            price_per_sequence[seq] = price

    return s, price_per_sequence


def part1(buyers):
    return sum(solve(int(n))[0] for n in buyers)


def part2(buyers):
    all_sequences = set()
    buyer_prices = []

    for n in buyers:
        _, price_per_seq = solve(int(n))
        all_sequences.update(price_per_seq.keys())
        buyer_prices.append(price_per_seq)

    best = None

    for seq in all_sequences:
        bananas = 0
        for price_per_seq in buyer_prices:
            if seq in price_per_seq:
                bananas += price_per_seq[seq]

        if best is None or best < bananas:
            best = bananas

    return best


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
    lines = [ln.strip() for ln in f.readlines()]

run("Part 1 with example data", lambda: part1(["1", "10", "100", "2024"]))
run("Part 1 with real input", lambda: part1(lines))
run("Part 2 with example data", lambda: part2(["1", "2", "3", "2024"]))
run("Part 2 with real input", lambda: part2(lines))
