
def realloc(banks):
    n = 0
    history = [list(banks)]
    while True:
        n += 1
        idx = banks.index(max(banks))
        v = banks[idx]
        banks[idx] = 0
        for _ in range(v):
            idx = (idx + 1) % len(banks)
            banks[idx] += 1
        if banks in history:
            return n, banks
        history.append(list(banks))


example_data = [0, 2, 7, 0]

with open("day6.txt") as fp:
    data = [int(x) for x in fp.read().split()]

n, banks = realloc(example_data)
assert n == 5
print(n)

n, banks = realloc(banks)
assert n == 4
print(n)

n, banks = realloc(data)
print(n)

n, banks = realloc(banks)
print(n)



