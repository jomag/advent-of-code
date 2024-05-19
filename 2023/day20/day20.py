from typing import List, Tuple


def part1(data, verbose=False):
    modules = {}
    states = {}
    for line in data:
        name, rest = line.split("->")
        name = name.strip()
        destinations = [s.strip() for s in rest.split(",")]
        if name[0] in "%&":
            kind, name = name[0], name[1:]
        else:
            kind, name = None, name
        modules[name] = (kind, destinations)
        if kind == "%":
            states[name] = False
        elif kind == "&":
            states[name] = {}
        else:
            states[name] = None

    for m in modules:
        mod = modules[m]
        for dest in mod[1]:
            if dest in modules and modules[dest][0] == "&":
                states[dest][m] = False

    def send_pulses(pulses: List[Tuple[str, bool, str]]):
        new_pulses: List[Tuple[str, bool, str]] = []
        for src, pulse, dst in pulses:
            if not dst in modules:
                continue
            mod = modules[dst]
            if mod[0] == "%":  # Flip-flop
                if not pulse:
                    states[dst] = not states[dst]
                    output = states[dst]
                    new_pulses.extend([(dst, output, a) for a in mod[1]])
            elif mod[0] == "&":  # Conjunction
                states[dst][src] = pulse
                output = not all(states[dst].values())
                new_pulses.extend([(dst, output, a) for a in mod[1]])
            elif mod[0] == None:  # Broadcaster module (initial)
                new_pulses.extend([(dst, pulse, a) for a in mod[1]])
            else:
                raise Exception(f"Unknown module type: {mod}")

        # for src, lvl, dst in new_pulses:
        #     s = "low" if not lvl else "high"
        #     print(f"{src} -{s}-> {dst}")

        return new_pulses

    low_count = 0
    high_count = 0

    n = 0
    while True:
        if n % 10_000 == 0:
            print(f"\nButton press {n+1}:")
        pulses: List[Tuple[str, bool, str]] = [("None", False, "broadcaster")]
        low_count += 1
        while len(pulses) > 0:
            pulses = send_pulses(pulses)
            for p in pulses:
                if p[1]:
                    high_count += 1
                else:
                    low_count += 1
            for p in pulses:
                if p[2] == "rx":
                    if not p[1]:
                        print(f"RX set to {p[1]} after {n} button presses")
                        input("Press enter to continue...")
        n += 1
        # input("Press enter to continue...")

    print("High pulse count:", high_count)
    print("Low pulse count:", low_count)

    return high_count * low_count


def part2(data, verbose=False):
    return 2


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
