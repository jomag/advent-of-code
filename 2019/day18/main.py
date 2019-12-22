from collections import deque
from PIL import Image, ImageDraw


def is_key(char):
    return char >= "a" and char <= "z"


def is_door(char):
    return char >= "A" and char <= "Z"


def find_character(maze, char):
    x = "".join(maze)
    w = len(maze[0])
    f = x.find(char)
    return (f % w, f // w)


def bfs(maze, start_symbol, target_symbol):
    w = len(maze[0])
    h = len(maze)
    edges = []
    x, y = find_character(maze, start_symbol)
    visited = [[False] * w for x in range(h)]
    queue = deque([(x, y, 0, [])])
    while queue:
        q = queue.popleft()
        x, y, distance, blocks = q
        if visited[y][x]:
            continue
        tile = maze[y][x]
        if tile == "#":
            continue
        if tile == target_symbol:
            return distance, blocks
        if tile.isalpha():
            if tile != start_symbol:
                blocks = blocks + [tile]
        visited[y][x] = True

        for dx, dy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if dx > 0 and dx < w - 1 and dy > 0 and dy < h - 1:
                if not visited[dy][dx]:
                    queue.append((dx, dy, distance + 1, blocks))


def get_reachable(maze, pos, collected):
    w = len(maze[0])
    h = len(maze)
    reachables = []
    x, y = pos
    visited = [[None] * w for x in range(h)]
    queue = deque([(x, y, 0)])
    while queue:
        q = queue.popleft()
        x, y, distance = q
        if visited[y][x] is not None:
            continue
        visited[y][x] = distance
        symbol = maze[y][x]
        if symbol == "#":
            continue
        if is_key(symbol) and symbol not in collected:
            reachables.append({"id": symbol, "distance": distance})
        if is_door(symbol) and symbol not in collected:
            if symbol.lower() not in collected:
                continue
            reachables.append({"id": symbol, "distance": distance})

        if symbol == "." or symbol in collected:
            if x > 0 and visited[y][x - 1] is None:
                queue.append((x - 1, y, distance + 1))
            if x < w - 1 and visited[y][x + 1] is None:
                queue.append((x + 1, y, distance + 1))
            if y > 0 and visited[y - 1][x] is None:
                queue.append((x, y - 1, distance + 1))
            if y < h - 1 and visited[y + 1][x] is None:
                queue.append((x, y + 1, distance + 1))

    # render_image(maze, visited, pos)
    # input()
    # sys.exit()
    return reachables


def render_image(maze, dmap, pos):
    sz = 10
    w = len(maze[0])
    h = len(maze)
    img = Image.new("RGB", (w * sz, h * sz))
    draw = ImageDraw.Draw(img)

    for y in range(h):
        for x in range(w):
            if pos[0] == x and pos[1] == y:
                c = (255, 255, 255)
                draw.rectangle(
                    [x * sz - 1, y * sz - 1, (x + 1) * sz - 1, (y + 1) * sz - 1], c
                )
            color = (255, 128, 64)
            tile = maze[y][x]
            distance = dmap[y][x]
            if tile == ".":
                if isinstance(distance, int):
                    v = (distance % 2) * 32 + 64
                    color = (v, (distance) % 255, (distance) % 255)
                else:
                    color = (128, 32, 32)
            elif tile == "@":
                color = (0, 0, 255)
            elif tile.isalpha():
                if tile.islower():
                    color = (32, 255, 64)
                else:
                    color = (255, 64, 32)
            draw.rectangle([x * sz, y * sz, (x + 1) * sz - 2, (y + 1) * sz - 2], color)
            if tile.isalpha():
                draw.text((x * sz + 2, y * sz - 2), tile, fill=(0, 0, 0))

    img.save("out.png", "PNG")


def get_reachable_precomputed(edges, start, collected):
    keys = [c for c in collected if c.islower()]
    edges = edges[start]
    reachable = []
    for sym, data in edges.items():
        if sym not in collected:
            distance, blocks = data
            locked = sym.isupper() and sym.lower() not in keys
            if not locked and all(block in collected for block in blocks):
                reachable.append({"id": sym, "distance": distance})
    return reachable


def solve(maze):
    cache = {}
    calls = 0
    skipped = 0

    def recurse(path):
        nonlocal calls, skipped, cache
        calls += 1

        if all(key in path for key in keys):
            return 0, path

        # keys_only = [c for c in path if c.islower()]
        # cache_key = "".join(sorted(path[:-1])) + f"->{path[-1]}"
        cache_key = "".join(sorted(path[:-1])) + f"->{path[-1]}"

        try:
            cached = cache[cache_key]
            skipped += 1
            return cached["distance"], cached["path"]
        except KeyError:
            pass

        start_position = find_character(maze, path[-1])
        # reachables = get_reachable(maze, start_position, path)
        reachables = get_reachable_precomputed(edges, path[-1], path)

        # print("PATH: ", path)
        # print("OLD: ", sorted(reachables1, key=lambda r: r["id"]))
        # print("NEW: ", sorted(reachables, key=lambda r: r["id"]))

        shortest = None
        reachables = sorted(reachables, key=lambda r: r["distance"])

        for reachable in reachables:
            distance, p = recurse(path + [reachable["id"]])
            distance += reachable["distance"]
            if shortest is None or distance < shortest:
                shortest = distance
                shortest_path = p

        cache[cache_key] = {"distance": shortest, "path": shortest_path}
        return shortest, shortest_path

    keys = [key for key in "".join(maze) if is_key(key)]
    doors = [door for door in "".join(maze) if is_door(door)]
    player = find_character(maze, "@")
    all_symbols = keys + doors + ["@"]

    for line in maze:
        print(line)

    # Edges is a dict with every symbol in the map
    # Every symbol has another dict with every symbol,
    # and the value of each is a tuple of distance
    # and doors blocking the path
    # { 'a': { 'b': (distance, ['C', 'D' ])}}
    print("Computing edges...")
    edges = {}
    for start in all_symbols:
        for target in all_symbols:
            if start != target and target != "@":
                if start not in edges:
                    edges[start] = {}
                edges[start][target] = bfs(maze, start, target)
    print("Done:")
    print(edges)

    keys = [key for key in "".join(maze) if is_key(key)]
    doors = [door for door in "".join(maze) if is_door(door)]
    player = find_character(maze, "@")

    print("Keys:  ", ", ".join(sorted(keys)))
    print("Doors: ", ", ".join(sorted(doors)))
    print("Player: ", player)

    shortest, path = recurse(["@"])

    print(f"Shortest: {shortest}")
    print(f"Shortest path: {':'.join(path)}")
    print(f"Cache: {len(cache)} items")
    print(f"Calls: {calls}, Skipped: {skipped}")


example1 = ["#########", "#b.A.@.a#", "#########"]

example2 = [
    "########################",
    "#f.D.E.e.C.b.A.@.a.B.c.#",
    "######################.#",
    "#d.....................#",
    "########################",
]
example3 = [
    "########################",
    "#...............b.C.D.f#",
    "#.######################",
    "#.....@.a.B.c.d.A.e.F.g#",
    "########################",
]
example4 = [
    "#################",
    "#i.G..c...e..H.p#",
    "########.########",
    "#j.A..b...f..D.o#",
    "########@########",
    "#k.E..a...g..B.n#",
    "########.########",
    "#l.F..d...h..C.m#",
    "#################",
]

example5 = [
    "########################",
    "#@..............ac.GI.b#",
    "###d#e#f################",
    "###A#B#C################",
    "###g#h#i################",
    "########################",
]

with open("input.txt", "r") as f:
    puzzleInput = [line.strip() for line in f.readlines()]

# solve(puzzleInput)

examples = [example1, example2, example3, example4, example5, puzzleInput]
for example in examples:
    solve(example)

