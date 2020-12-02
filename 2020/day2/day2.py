def validate1(line):
    tokens = line.split(" ")
    a, b = [int(s) for s in tokens[0].split("-")]
    c = tokens[1][0]
    pwd = tokens[2]
    n = sum(1 for x in pwd if x == c)
    return n >= a and n <= b


def validate2(line):
    tokens = line.split(" ")
    a, b = [int(s) - 1 for s in tokens[0].split("-")]
    c = tokens[1][0]
    pwd = tokens[2]
    return (pwd[a] == c and pwd[b] != c) or (pwd[a] != c and pwd[b] == c)


with open("input") as f:
    lines = f.readlines()
    valid1 = sum(1 for line in lines if validate1(line))
    valid2 = sum(1 for line in lines if validate2(line))
    print(f"Valid count 1: {valid1}")
    print(f"Valid count 2: {valid2}")
