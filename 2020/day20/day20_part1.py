import sys, re, math


def parse_tile(text):
    lines = text.split("\n")
    header = lines[0]
    tile = lines[1:]

    m = re.match("Tile (\\d+):", header)
    assert m, "invalid tile header line"
    assert len(tile) == 10, f"not 10: {len(tile)}"
    assert all(len(line) == 10 for line in tile)

    i = int(m.group(1))
    a = tile[0]
    b = "".join(l[9] for l in tile)
    c = tile[9][::-1]
    d = "".join([l[0] for l in tile])[::-1]
    return i, [a, b, c, d]


tiles = {}

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    content = f.read()

for t in content.split("\n\n"):
    tile, edges = parse_tile(t)
    tiles[tile] = edges

corners = []

for c, edges in tiles.items():
    adj = 0
    for t, t_edges in tiles.items():
        if t != c:
            for edge in t_edges:
                adj += sum(1 for e in edges if e == edge or e == edge[::-1])
    if adj == 2:
        corners.append(c)

print(f"Part 1: {math.prod(corners)}")
