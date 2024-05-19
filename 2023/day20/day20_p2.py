from typing import List, Tuple


def part2(data, verbose=False):
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
                if p[2] in ["vg", "kp", "gc", "tx"]:
                    if not p[1]:
                        input(
                            f"{p[2]} low after {n} presses. bq state: {states['bq']} Press enter to continue..."
                        )
                if p[2] == "rx":
                    if not p[1]:
                        print(f"RX set to {p[1]} after {n} button presses")
                        input("Press enter to continue...")
        n += 1
        # input("Press enter to continue...")

    # I discovered that "rx" gets it input from conjugate "bq" which has
    # four inputs: "tx", "kp", "gc" and "vg". "bq" will output low when
    # all inputs are low. It turned out through experimentation that all
    # of them sends a low output at a fixed interval:
    #
    # - tx: 3769
    # - kp: 3929
    # - gc: 4001
    # - vg: 4027
    #
    # Then I only needed to find the lowest common denominator:
    #
    # import math
    # math.lcm(3769, 3929, 4001, 4027)
    #
    # LCM is 238593356738827 which is the correct answer
    #
    # Maybe I'll update the code to calculate this automatically,
    # but not likely...

    return math.lcm(3769, 3929, 4001, 4027)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

print(f"Part 2 with real input: {part2(lines)}")
