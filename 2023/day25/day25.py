import time

# After failing to come up with an automated way to find
# the dividing pairs, I exported a Graphviz graph and 
# used the builtin "neato" command to immediately find
# the three pairs.
#
# I already had a method to count sizes of the groups
# which worked on the example, so from then on it
# was easy.
#
# To view the graphs, first run the export (see end of
# file) and then view the exported graph with this
# command:
#
# neato vis.dot -T svg -o vis.svg

def parse(data):
    schematics = {}
    for line in data:
        if ":" in line:
            c, ref = line.split(":")
            assert len(c) == 3
            ref = [s.strip() for s in ref.split(" ") if s.strip()]
            schematics[c] = tuple(ref)
    return schematics


def solve(data, disconnects):
    pairs = set()

    for k, v in data.items():
        for w in v:
            pairs.add(tuple(sorted([k, w])))

    def build_groups(conn):
        groups = []
        visited_components = set()
        for c in conn:
            if c in visited_components:
                continue

            current_group = set([c])
            q = [c]

            while q:
                c = q.pop()
                current_group.add(c)
                visited_components.add(c)
                for cc in conn[c]:
                    if cc not in visited_components and cc not in q:
                        q.append(cc)

            groups.append(current_group)
        return groups

    def build_conn(pairs, disconnected_pairs):
        conn = {}
        for a, b in pairs:
            if (a, b) in disconnected_pairs or (b, a) in disconnected_pairs:
                continue
            if a in conn:
                conn[a].add(b)
            else:
                conn[a] = set([b])
            if b in conn:
                conn[b].add(a)
            else:
                conn[b] = set([a])
        return conn

    groups = build_groups(build_conn(pairs, disconnects))
    assert len(groups) == 2
    return len(groups[0]) * len(groups[1])


def export_graph(data, filename):
    graph = ["graph G {\n"]
    for k, v in data.items():
        for vv in v:
            graph.append(f"{k} -- {vv};\n")
    graph.append("}\n")

    with open(filename, "w") as f:
        f.writelines(graph)


def run(label, f):
    start = time.perf_counter()
    result = f()
    elapsed = time.perf_counter() - start
    if elapsed > 2:
        elapsed = f"{elapsed:.3f}s"
    else:
        elapsed = f"{elapsed*1000:.1f}ms"
    print(f"{label}: {result} ({elapsed})")


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

lines = parse(lines)
example = parse(example)

# export_graph(example, "example.dot")
# export_graph(lines, "vis.dot")

example_disconnects = [("hfx", "pzl"), ("bvb", "cmg"), ("nvd", "jqt")]
input_disconnects = [("ttv", "ztc"), ("bdj", "vfh"), ("bnv", "rpd")]

run("Part 1 with example data", lambda: solve(example, example_disconnects))
run("Part 1 with real input", lambda: solve(lines, input_disconnects))
