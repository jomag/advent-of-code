
import binascii
from functools import reduce


def sparse_hash(count, lengths, reps=1):
    v = list(range(count))
    pos = 0
    skip_size = 0

    for rep in range(reps):
        for length in lengths:
            begin = pos
            end = pos + length - 1

            for _ in range(length // 2):
                bm = begin % count
                em = end % count
                v[bm], v[em] = v[em], v[bm]
                begin += 1
                end -= 1
        
            pos = (pos + length + skip_size) % count
            skip_size += 1

    return v


def dense_hash(data):
    h = []
    for i in range(16):
        h.append(reduce(lambda i, j: i ^ j, data[i*16:(i+1)*16]))
    return h


def part2(data):
    lengths = [ord(b) for b in data] + [17, 31, 73, 47, 23]
    dense = dense_hash(sparse_hash(256, lengths, 64))
    return binascii.hexlify(bytes(dense)).decode()


with open("day10.txt") as f:
    data = f.read()
    
assert sparse_hash(5, [3, 4, 1, 5]) == [3, 4, 2, 1, 0]

part1_data = [int(n) for n in data.split(",")]
sparse = sparse_hash(256, part1_data)
print(sparse[0] * sparse[1])


assert part2("") == "a2582a3a0e66e6e86e3812dcb672a272"
assert part2("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
assert part2("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
assert part2("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"
print(part2(data))

