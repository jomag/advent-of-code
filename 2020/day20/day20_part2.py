# Todays part 2 was not exactly hard, but it was a very large task.
# This is by far the ugliest code so far in this years AoC, but
# I can not be bothered to clean it up. The final rotation and
# flipping was found by experimentation.

import sys, re, math


def rotate(data):
    assert len(data[0]) == len(data)
    return ["".join(l[i] for l in data[::-1]) for i in range(len(data))]


def flip(data):
    return [l[::-1] for l in data]


class Tile:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.pos = None

    def rotate(self):
        self.data = rotate(self.data)

    def flip(self):
        self.data = flip(self.data)

    def print(self):
        print(f"Tile {self.name}")
        for line in self.data:
            print(line)

    def top_edge(self):
        return self.data[0]

    def right_edge(self):
        return "".join(l[-1] for l in self.data)

    def bottom_edge(self):
        return self.data[-1]

    def left_edge(self):
        return "".join(l[0] for l in self.data)


def parse_tile(text):
    lines = text.split("\n")
    header = lines[0]
    tile = lines[1:]

    m = re.match("Tile (\\d+):", header)
    assert m, "invalid tile header line"
    assert len(tile) == 10, f"not 10: {len(tile)}"
    assert all(len(line) == 10 for line in tile)

    return Tile(int(m.group(1)), tile)


tiles = set()
placed = set()

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    content = f.read()

for t in content.split("\n\n"):
    tiles.add(parse_tile(t))


def find_tile(pos):
    for tile in placed:
        if pos == tile.pos:
            return tile
    return None


def place_tiles(pos, tile):
    # Add tile to list of placed tiles
    tile.pos = pos
    placed.add(tile)
    tiles.remove(tile)

    # Check if all have been placed
    if len(tiles) == 0:
        return

    # Place tile above current one
    adj_pos = (pos[0], pos[1] - 1)
    adj = find_tile(adj_pos)
    if not adj:
        edge = tile.top_edge()
        for a in tiles:
            if a.bottom_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.bottom_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.bottom_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.bottom_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.flip()
            if a.bottom_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.bottom_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.bottom_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.bottom_edge() == edge:
                place_tiles(adj_pos, a)
                break

    # Place tile to the right of the current one
    adj_pos = (pos[0] + 1, pos[1])
    adj = find_tile(adj_pos)
    if not adj:
        edge = tile.right_edge()
        for a in tiles:
            if a.left_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.left_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.left_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.left_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.flip()
            if a.left_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.left_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.left_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.left_edge() == edge:
                place_tiles(adj_pos, a)
                break

    # Place tile below the current one
    adj_pos = (pos[0], pos[1] + 1)
    adj = find_tile(adj_pos)
    if not adj:
        edge = tile.bottom_edge()
        for a in tiles:
            if a.top_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.top_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.top_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.top_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.flip()
            if a.top_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.top_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.top_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.top_edge() == edge:
                place_tiles(adj_pos, a)
                break

    # Place tile to the right of the current one
    adj_pos = (pos[0] - 1, pos[1])
    adj = find_tile(adj_pos)
    if not adj:
        edge = tile.left_edge()
        for a in tiles:
            if a.right_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.right_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.right_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.right_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.flip()
            if a.right_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.right_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.right_edge() == edge:
                place_tiles(adj_pos, a)
                break
            a.rotate()
            if a.right_edge() == edge:
                place_tiles(adj_pos, a)
                break


# for t in tiles:
#     if t.name == 1951:
#         t.flip()
#         t.rotate()
#         t.rotate()
#         place_tiles((0, 0), t)
#         break
first = tiles.pop()
tiles.add(first)
place_tiles((0, 0), first)

top = min(t.pos[1] for t in placed)
bottom = max(t.pos[1] for t in placed)
left = min(t.pos[0] for t in placed)
right = max(t.pos[0] for t in placed)

for y in range(top, bottom + 1):
    for y2 in range(10):
        for x in range(left, right + 1):
            t = find_tile((x, y))
            if not t:
                print("?????????? ", end="")
            else:
                print(f"{t.data[y2]} ", end="")
        print()
    print()


puzzle = []

for y in range(top, bottom + 1):
    for y2 in range(1, 9):
        s = ""
        for x in range(left, right + 1):
            t = find_tile((x, y))
            s += t.data[y2][1:9]
        puzzle.append(s)

# This sequence was found by experimentation, testing
# all 8 possible mutations of the puzzle. Later I found
# that the sequence is actually random, as it depends
# on in what order the tiles in the sets were iterated.

# puzzle = flip(puzzle)
puzzle = rotate(puzzle)
# puzzle = rotate(puzzle)
# puzzle = rotate(puzzle)

# Find monster
monster = ["                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "]

monster_width = max(len(l) for l in monster)
monster_height = len(monster)

puzzle_width = len(puzzle[0])
puzzle_height = len(puzzle)

for y in range(0, puzzle_height - monster_height):
    for x in range(0, puzzle_width - monster_width):
        valid = True
        for cy in range(monster_height):
            for cx in range(monster_width):
                if monster[cy][cx] == "#":
                    if puzzle[y + cy][x + cx] != "#":
                        valid = False
                        break
            if not valid:
                break
        if valid:
            for cy in range(monster_height):
                for cx in range(monster_width):
                    if monster[cy][cx] == "#":
                        s = list(puzzle[y + cy])
                        s[x + cx] = "O"
                        puzzle[y + cy] = "".join(s)

print("Final result:")
print("\n".join(puzzle))

part2 = sum(1 for c in "".join(puzzle) if c == "#")
print(f"Part 2: {part2}")