import sys, re, json

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    rules = f.readlines()

bags = {}

for rule in rules:
    m = re.findall("^(.*) bags contain ([^.]+)\.$", rule.strip())
    bag_name = m[0][0]
    content = m[0][1]
    content = re.findall("\s*(\d+) (.*?)\s+bags?,?\s*", content)
    content = [(int(c[0]), c[1]) for c in content if len(c) > 0]
    bags[bag_name] = {c[1]: c[0] for c in content}


def get_holders(bag):
    immediate_holders = set()

    for parent_name, children in bags.items():
        if bag in children.keys():
            immediate_holders.add(parent_name)

    holders = set().union(immediate_holders)

    for h in immediate_holders:
        holders = holders.union(get_holders(h))

    return holders


def total_bag_count(bag):
    return sum(total_bag_count(name) * cnt for name, cnt in bags[bag].items()) + 1


part1 = len(get_holders("shiny gold"))
print(f"Part 1: {part1}")

part2 = total_bag_count("shiny gold") - 1
print(f"Part 2: {part2}")