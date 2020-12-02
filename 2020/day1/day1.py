with open("input", "r") as f:
    v = [int(line) for line in f.readlines()]

i = 0
for n in v:
    i += 1
    for m in v[i:]:
        if n + m == 2020:
            print(f"{n} + {m} = {n * m}")
            break

i = 0
for n in v:
    i += 1
    j = 0
    for m in v[i:]:
        j += 1
        for o in v[j:]:
            if n + m + o == 2020:
                print(f"{n} + {m} + {o} = {n * m * o}")
                break
