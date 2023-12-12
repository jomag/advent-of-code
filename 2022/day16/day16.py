# Note that I only solved part one for day 16 2022!

from functools import cache
import re
from typing import Any


class Valve:
    def __init__(self, name: str, rate: int, tunnels: list[str]):
        self.name = name
        self.rate = rate
        self.tunnels = tunnels

    def print(self):
        print(f"{self.name}: rate={self.rate}, tunnels={', '.join(self.tunnels)}")


def parse(lines):
    p = re.compile(
        r"Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z][A-Z, ]*)"
    )
    valves = {}
    for line in lines:
        m = p.findall(line)[0]
        tunnels = m[2].split(", ")
        valves[m[0]] = Valve(m[0], int(m[1]), tunnels)
    return valves


def part1(valves, verbose=False):
    @cache
    def move_to(name, elapsed_time, open_valves: str, rate, pressure):
        # print(open_valves)

        if elapsed_time >= 30:
            return pressure

        valve = valves[name]
        highest = 0

        if name not in open_valves and valve.rate > 0:
            ov = " ".join(sorted((*open_valves.split(), name)))
            h2 = move_to(
                name,
                elapsed_time + 1,
                ov,
                rate + valve.rate,
                pressure + rate,
            )
            highest = max(highest, h2)

        valve = valves[name]
        for v in valve.tunnels:
            h1 = move_to(v, elapsed_time + 1, open_valves, rate, pressure + rate)
            highest = max(highest, h1)

        return highest

    h = move_to("AA", 0, "", 0, 0)
    return h


def part2(valves, verbose=False):
    cache = {}
    valves_with_non_zero_rate = 6

    def move_to(my_name, ele_name, remaining, open_valves: set[str], rate, pressure):
        my_name, ele_name = sorted((my_name, ele_name))
        cache_key = f"{my_name}|{ele_name}|{','.join(open_valves)}"

        try:
            cache_item = cache[cache_key]
            if remaining <= cache_item["remaining"]:
                return cache_item["pressure"]
        except KeyError:
            cache_item = None

        if remaining <= 0:
            if cache_item is None or (
                cache_item["remaining"] == 0 and cache_item["pressure"] < pressure
            ):
                cache[cache_key] = {"remaining": 0, "pressure": pressure}
            return pressure

        if len(open_valves) >= valves_with_non_zero_rate:
            p = (remaining - 1) * rate + pressure
            if cache_item is None or cache_item["pressure"] < p:
                cache[cache_key] = {"remaining": remaining, "pressure": p}
            return p

        my_valve = valves[my_name]
        ele_valve = valves[ele_name]
        highest = 0

        if my_name not in open_valves and my_valve.rate > 0:
            if (
                my_name != ele_name
                and ele_name not in open_valves
                and ele_valve.rate > 0
            ):
                h2 = move_to(
                    my_name,
                    ele_name,
                    remaining - 1,
                    set((*open_valves, my_name, ele_name)),
                    rate + my_valve.rate + ele_valve.rate,
                    pressure + rate,
                )
                highest = max(highest, h2)
            else:
                ov = set((*open_valves, my_name))
                for ele_next in ele_valve.tunnels:
                    name1, name2 = sorted((my_name, ele_next))
                    highest = max(
                        highest,
                        move_to(
                            name1,
                            name2,
                            remaining - 1,
                            ov,
                            rate + my_valve.rate,
                            pressure + rate,
                        ),
                    )
        elif ele_name not in open_valves and ele_valve.rate > 0:
            ov = set((*open_valves, ele_name))
            for my_next in my_valve.tunnels:
                name1, name2 = sorted((my_next, ele_name))
                highest = max(
                    highest,
                    move_to(
                        name1,
                        name2,
                        remaining - 1,
                        ov,
                        rate + ele_valve.rate,
                        pressure + rate,
                    ),
                )

        for ele_next in ele_valve.tunnels:
            for my_next in my_valve.tunnels:
                name1, name2 = sorted((my_next, ele_next))
                highest = max(
                    highest,
                    move_to(
                        name1,
                        name2,
                        remaining - 1,
                        open_valves,
                        rate,
                        pressure + rate,
                    ),
                )

        if cache_item is None or cache_item["pressure"] < highest:
            cache[cache_key] = {"remaining": remaining, "pressure": highest}
        return highest

    h = move_to("AA", "AA", 25, set(), 0, 0)
    return h


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(parse(example), verbose=True)}")
# print(f"Part 1 with real input: {part1(parse(lines))}")
print(f"Part 2 with example data: {part2(parse(example), verbose=True)}")
# print(f"Part 2 with real input: {part2(parse(lines))}")
