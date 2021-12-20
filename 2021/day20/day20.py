class Image:
    def __init__(self, bitmap):
        self.bitmap = bitmap
        self.width = len(bitmap[0])
        self.height = len(bitmap)
        self.buf = [["?" for _ in range(self.width)] for _ in range(self.height)]
        self.undefined = "."

    def grow(self, n):
        w, h = self.width, self.height
        nw, nh = w + n + n, h + n + n
        self.buf = [["?" for _ in range(nw)] for _ in range(nh)]
        bmp = [[self.undefined for _ in range(nw)] for _ in range(nh)]
        for x in range(w):
            for y in range(h):
                bmp[y + n][x + n] = self.bitmap[y][x]
        self.width = nw
        self.height = nh
        self.bitmap = bmp

    def print(self):
        for line in self.bitmap:
            print("".join(p for p in line))

    def at(self, x, y):
        try:
            return self.bitmap[y][x]
        except IndexError:
            return self.undefined

    def get_algo_index_at(self, x, y):
        bits = [
            self.at(xx, yy) for yy in range(y - 1, y + 2) for xx in range(x - 1, x + 2)
        ]
        ptr = 0
        for bit in bits:
            ptr = (ptr << 1) + (1 if bit == "#" else 0)
        return ptr

    def apply(self, algo):
        for y in range(0, self.height):
            for x in range(0, self.width):
                ptr = self.get_algo_index_at(x, y)
                self.buf[y][x] = algo[ptr]

        self.bitmap, self.buf = self.buf, self.bitmap

        if algo[0] == "#":
            self.undefined = "." if self.undefined == "#" else "#"

    def lit_count(self):
        if self.undefined == "#":
            raise Exception("Infinite!")
        return sum(1 for line in self.bitmap for p in line if p == "#")


def parse(data):
    algo = data[0]
    image = Image([[pixel for pixel in line] for line in data[2:]])
    return algo, image


def part1(data, steps, verbose=False):
    algo, image = parse(data)
    image.grow(steps)

    for _ in range(steps):
        image.apply(algo)

    if verbose:
        image.print()

    return image.lit_count()


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data: {part1(example, steps=2,verbose=False)}")
print(f"Part 1 with real input: {part1(lines, steps=2,verbose=False)}")
print(f"Part 2 with example data: {part1(example, steps=50, verbose=False)}")
print(f"Part 2 with real input: {part1(lines, steps=50,verbose=False)}")
