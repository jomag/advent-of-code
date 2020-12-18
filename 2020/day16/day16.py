import sys, re, math


def validate_with_rule(r, v):
    return (v >= r[0] and v <= r[1]) or (v >= r[2] and v <= r[3])


def validate_ticket_value(rules, v):
    return any(validate_with_rule(r, v) for r in rules.values())


def validate_ticket(rules, ticket):
    for v in ticket:
        if not validate_ticket_value(rules, v):
            return False
    return True


def validate(rules, ticket, nearby):
    invalid = []
    for t in [ticket] + nearby:
        for v in t:
            if not validate_ticket_value(rules, v):
                invalid.append(v)
    return invalid


def determine_order(rules, tickets):
    remaining = {k: v for k, v in rules.items()}
    order = []

    # Step 1: find all rules that validate all values in each column
    while len(order) < len(rules.keys()):
        n = len(order)
        order.append([])
        for rk, rv in list(remaining.items()):
            if all(validate_with_rule(rv, t[n]) for t in tickets):
                order[n].append(rk)

    # Step 2: find a single rule for each column by searching for
    # columns that has only one possible rule, and removing that rule
    # from all other columns
    done = False
    while not done:
        print(f"Before: {order}")
        done = True
        with_single_option = [o for o in order if len(o) == 1]
        for o in with_single_option:
            print(f"Dropping: {o}")
            for u in order:
                if len(u) > 1:
                    try:
                        del u[u.index(o[0])]
                        done = False
                    except ValueError:
                        pass

    return order


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    lines = f.readlines()

rules = {}
ticket = []
nearby = []

g = 0
for line in lines:
    line = line.strip()
    if line == "your ticket:":
        g = 1
    elif line == "nearby tickets:":
        g = 2
    elif line == "":
        pass
    elif g == 0:
        m = re.match("([a-z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)", line)
        assert m is not None, f"Invalid rule: {line}"
        m = m.groups()
        assert len(m) == 5
        rules[m[0]] = [int(n) for n in m[1:]]
    elif g == 1:
        ticket = [int(n) for n in line.split(",")]
    elif g == 2:
        nearby.append([int(n) for n in line.split(",")])


print(f"Part 1: {sum(validate(rules, ticket, nearby))}")

valid_tickets = [t for t in [ticket] + nearby if validate_ticket(rules, t)]
order = determine_order(rules, valid_tickets)

departure_fields = [
    ticket[n] for n in range(len(order)) if order[n][0].startswith("departure")
]

part2 = math.prod(departure_fields)
print(f"Part 2: {part2}")
