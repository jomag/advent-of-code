
def run(n):
    # Possibly not very efficient with O(n) complexity, but it works...
    x, y = 0, 0
    i = 1
    side_length = 0
    offs = 1
    
    while i < n:
        idx = i - offs
        if idx < side_length:
            y = y - 1
        elif idx < side_length * 2:
            x = x - 1
        elif idx < side_length * 3:
            y = y + 1
        elif idx < side_length * 4:
            x = x + 1
        else:
            side_length += 2
            offs = i
            x = x + 1
        i = i + 1

    return abs(x) + abs(y)


def run_part2(n):
    x, y = 0, 0
    i = 1
    side_length = 0
    offs = 1
    tbl = {(0, 0): 1}

    while True:
        idx = i - offs
        if idx < side_length:
            y = y - 1
        elif idx < side_length * 2:
            x = x - 1
        elif idx < side_length * 3:
            y = y + 1
        elif idx < side_length * 4:
            x = x + 1
        else:
            side_length += 2
            offs = i
            x = x + 1

        neighbours = [
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)
        ]

        nsum = sum(tbl[v] for v in neighbours if v in tbl)
        
        if nsum > n:
            return nsum
        
        tbl[(x, y)] = nsum
        i = i + 1
        

for ex in [1, 12, 23, 1024, 289326]:
    print("%d -> %d" % (ex, run(ex)))

for ex in [289326]:
    print("%d @ %d" % (ex, run_part2(ex)))

