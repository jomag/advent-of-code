import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    ts = int(f.readline())
    ids = [int(b) if b != "x" else None for b in f.readline().split(",")]

shortest = None
shortest_id = None
for n in ids:
    if n is not None:
        waiting_time = n - ts % n
        if shortest is None or shortest > waiting_time:
            shortest = waiting_time
            shortest_id = n

print(f"Part 1: {shortest_id * shortest}")

offsets = []
n = 0
for i in range(len(ids)):
    if ids[i] is not None:
        offsets.append(n)
    n += 1

ids = [i for i in ids if i is not None]

print(f"offsets: {offsets}")
print(f"ids:     {ids}")

# Explanation of algorithm:
#
# We step through all the busses in order, and find the first possible time:
#
# If only first bus is considered, the first time is obviously 0. Another
# bus leaves at 0+id, 0+id+id, and so on
#
# For the second bus, the first possible time is the first time of previous
# bus (0) plus the offset of the second bus. If not a match, then next possible
# time is the next time of previous bus: 0 + id. Repeat until a time "t" is found
# where the second bus leaves at correct offset compared to first bus.
#
# For the third bus, the first possible time is the first time of the second bus.
# Same procedure as for second bus is reapeated, except that the interval is set
# to the previous bus intervals multiplied with each other.
#
# Example: id 17 at offset 0, id 13 at offset 2, id 19 at offset 3
#
# We start with "t" set to 0, as that's the obvious first time the first bus
# leaves.
#
# Next bus, 13, also leaves at 0, but it does not match the offset constraint of 2.
# So we try each start of bus 17 until a valid time is found. We find that
# the 6'th start of bus 17 will be followed by bus 13 at correct offset, so
# "t" is set to 6 * 17 = 102. The next opportunity is 17 * 13 time units later (323).
#
# Same procedure is repeated for the third bus, 19. Time 102 is not a match for
# its offset constraint, and neither is 323. The first time where the offset
# constraint is met is at 3417 and this is the solution for this example.

p = ids[0]
t = 0

for i in range(1, len(offsets)):
    while (t + offsets[i]) % ids[i] != 0:
        t += p
    p = p * ids[i]

print(f"Part 2: {t}")
