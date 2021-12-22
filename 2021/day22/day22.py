from typing import List, Tuple


class Cube:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
        self.z1, self.z2 = z1, z2

    @property
    def volume(self):
        w = self.x2 + 1 - self.x1
        h = self.y2 + 1 - self.y1
        d = self.z2 + 1 - self.z1
        return w * h * d

    def contains(self, o):
        if self.x1 <= o.x1 and self.x2 >= o.x2:
            if self.y1 <= o.y1 and self.y2 >= o.y2:
                if self.z1 <= o.z1 and self.z2 >= o.z2:
                    return True
        return False

    def intersects(self, o):
        if o.x1 > self.x2 or o.x2 < self.x1:
            return False
        if o.y1 > self.y2 or o.y2 < self.y1:
            return False
        if o.z1 > self.z2 or o.z2 < self.z1:
            return False
        return True

    def equal(self, o):
        return (
            self.x1 == o.x1
            and self.x2 == o.x2
            and self.y1 == o.y1
            and self.y2 == o.y2
            and self.z1 == o.z1
            and self.z2 == o.z2
        )

    def split_x(self, o):
        cubes = []

        if o.x1 < self.x1 and o.x2 >= self.x1:
            cubes.append(Cube(o.x1, self.x1 - 1, o.y1, o.y2, o.z1, o.z2))
            o = Cube(self.x1, o.x2, o.y1, o.y2, o.z1, o.z2)

        if o.x1 <= self.x2 and o.x2 > self.x2:
            cubes.append(Cube(o.x1, self.x2, o.y1, o.y2, o.z1, o.z2))
            o = Cube(self.x2 + 1, o.x2, o.y1, o.y2, o.z1, o.z2)

        return cubes + [o]

    def split_y(self, o):
        cubes = []

        if o.y1 < self.y1 and o.y2 >= self.y1:
            cubes.append(Cube(o.x1, o.x2, o.y1, self.y1 - 1, o.z1, o.z2))
            o = Cube(o.x1, o.x2, self.y1, o.y2, o.z1, o.z2)

        if o.y1 <= self.y2 and o.y2 > self.y2:
            cubes.append(Cube(o.x1, o.x2, o.y1, self.y2, o.z1, o.z2))
            o = Cube(o.x1, o.x2, self.y2 + 1, o.y2, o.z1, o.z2)

        return cubes + [o]

    def split_z(self, o):
        cubes = []

        if o.z1 < self.z1 and o.z2 >= self.z1:
            cubes.append(Cube(o.x1, o.x2, o.y1, o.y2, o.z1, self.z1 - 1))
            o = Cube(o.x1, o.x2, o.y1, o.y2, self.z1, o.z2)

        if o.z1 <= self.z2 and o.z2 > self.z2:
            cubes.append(Cube(o.x1, o.x2, o.y1, o.y2, o.z1, self.z2))
            o = Cube(o.x1, o.x2, o.y1, o.y2, self.z2 + 1, o.z2)

        return cubes + [o]

    def split(self, o):
        cubes = self.split_x(o)
        cubes = [cc for c in cubes for cc in self.split_y(c)]
        cubes = [cc for c in cubes for cc in self.split_z(c)]
        return [c for c in cubes if not self.contains(c)]

    def __repr__(self):
        return f"|{self.x1}..{self.x2}, {self.y1}..{self.y2}, {self.z1}..{self.z2}|"


class CubeSet:
    def __init__(self):
        self.cubes = []

    def add(self, cube):
        for c in self.cubes:
            if c.contains(cube):
                return
            if cube.intersects(c):
                new_cubes = c.split(cube)
                for ccc in new_cubes:
                    self.add(ccc)
                return

        self.cubes.append(cube)

    def remove(self, cube):
        cubelist = []
        for c in self.cubes:
            if not cube.contains(c):
                cubelist.append(c)
        self.cubes = cubelist

        cubelist = []
        for c in self.cubes:
            if c.intersects(cube):
                cubelist.extend(cube.split(c))
            else:
                cubelist.append(c)
        self.cubes = cubelist

    @property
    def volume(self):
        return sum(cube.volume for cube in self.cubes)

    def print(self):
        print(f"{len(self.cubes)} cubes:")
        for c in self.cubes:
            print(f"- {c}")


def parse(data: List[str]):
    ops = []
    for line in data:
        act, rest = line.split(" ")
        sx, sy, sz = rest.split(",")
        sx = sx[2:].split("..")
        sy = sy[2:].split("..")
        sz = sz[2:].split("..")
        cube = Cube(
            int(sx[0]),
            int(sx[1]),
            int(sy[0]),
            int(sy[1]),
            int(sz[0]),
            int(sz[1]),
        )
        ops.append((act, cube))
    return ops


def solve(data, limit=None, verbose=False):
    ops = parse(data)

    if limit:
        ops = [
            op
            for op in ops
            if abs(op[1].x1) <= limit
            and abs(op[1].x2) <= limit
            and abs(op[1].y1) <= limit
            and abs(op[1].y2) <= limit
            and abs(op[1].z1) <= limit
            and abs(op[1].z2) <= limit
        ]

    cubes = CubeSet()
    for n, op in enumerate(ops):
        if verbose:
            print(f"{n+1} / {len(ops)}: {op}")
        if op[0] == "on":
            cubes.add(op[1])
        else:
            cubes.remove(op[1])

    return cubes.volume


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example1.txt") as f:
    example1 = [ln.strip() for ln in f.readlines()]

with open("example2.txt") as f:
    example2 = [ln.strip() for ln in f.readlines()]

print(f"Part 1 with example data 1: {solve(example1,limit=50, verbose=False)}")
print(f"Part 1 with real input: {solve(lines,limit=50)}")

print(f"Part 2 with example data 1: {solve(example2, limit=50,verbose=False)}")
print(f"Part 2 with example data 2: {solve(example2,  verbose=False)}")
print(f"Part 2 with real input: {solve(lines)}")
