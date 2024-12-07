def parse(data):
    eq = []
    for line in data:
        testval, rest = line.split(":")
        nums = [int(s) for s in rest.split(" ") if s.strip()]
        eq.append((int(testval), nums))
    return eq


def part1(data):
    sum = 0

    for eq in data:
        testval, nums = eq
        for bitmap in range(1 << len(nums) - 1):
            res = nums[0]
            for n in nums[1:]:
                if bitmap & 1:
                    res = res * n
                else:
                    res = res + n
                bitmap = bitmap >> 1
            if res == testval:
                sum += testval
                break

    return sum


def part2(data):
    def rec(testval, a, nums):
        if len(nums) == 0:
            return testval == a
        if rec(testval, a + nums[0], nums[1:]):
            return True
        if rec(testval, a * nums[0], nums[1:]):
            return True
        if rec(testval, int(str(a) + str(nums[0])), nums[1:]):
            return True
        return False

    sum = 0
    for eq in data:
        testval, nums = eq
        if rec(testval, nums[0], nums[1:]):
            sum += testval

    return sum


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

print(f"Part 1 with example data: {part1(example)}")
print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example)}")
print(f"Part 2 with real input: {part2(lines)}")
