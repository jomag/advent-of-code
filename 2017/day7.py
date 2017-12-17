# There's an error in this solution: it returns two misbalanced nodes for part 2.
# The second one is the correct one. 

def parse(text):
    nodes = {}
    for line in text.splitlines():
        parts = line.split()
        name = parts[0]
        weight = int(parts[1].strip("()"))
        nodes[name] = { "name": name, "weight": weight, "children": [], "parent": None }
        if len(parts) > 2:
            assert parts[2] == "->"
            nodes[name]["children"] = [c.strip(",") for c in parts[3:]]

    for node in nodes.values():
        node["children"] = [nodes[name] for name in node["children"]]
        for child in node["children"]:
            child["parent"] = node

    for node in nodes.values():
        if node["parent"] is None:
            return node

    raise RuntimeError("No root found")


def part2(node):
    def total_weight(node):
        return node["weight"] + sum(total_weight(c) for c in node["children"])

    c1 = None
    c2 = None

    for c in node["children"]:
        if c1 is None:
            c1 = c
        elif c2 is None:
            if total_weight(c1) != total_weight(c):
                c2 = c
        else:
            if total_weight(c) != total_weight(c1):
                good_node, bad_node = c2, c1
            else:
                good_node, bad_node = c1, c2
                    
            print("Unbalanced child found: %s" % bad_node["name"])
            print("Total weight: %d" % total_weight(bad_node))
            print("Total weight should be: %d" % total_weight(good_node))

            diff = total_weight(good_node) - total_weight(bad_node)
            print("The node weight should be: %d" % (bad_node["weight"] + diff))
            
            weights = ["%s: %d" % (n["name"], total_weight(n)) for n in node["children"]]
            print("All weights: " + str(weights))
            print("Parent: " + node["name"])
            print()
            break

    for c in node["children"]:
        part2(c)


example_data = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""

with open("day7.txt") as f:
    input_data = f.read()

root = parse(example_data)
assert root["name"] == "tknk"

print("With example data:\n")
part2(root)

print("With input data:\n")
root = parse(input_data)
print("Root: %s\n" % root["name"])

part2(root)

