import sys


def find_invalid(preamble: int, nums: list):
    for i in range(preamble, len(nums)):
        pre = nums[i - preamble : i]
        combos = [a + b for a in pre for b in pre]
        if nums[i] not in combos:
            return i, nums[i]


def find_weakness(trg: int, nums: list):
    for i in range(len(nums)):
        for j in range(len(nums) - i):
            if sum(nums[i:j]) == trg:
                return min(nums[i:j]) + max(nums[i:j])


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
preamble = int(sys.argv[2]) if len(sys.argv) > 2 else 25
with open(filename) as f:
    numbers = [int(line) for line in f.readlines()]

res = find_invalid(preamble, numbers)
assert res, "No invalid found"
print(f"Part 1: {res[1]} at index {res[0]}")

weakness = find_weakness(res[1], numbers)
print(f"Part 2: {weakness}")
