def part1(data, verbose=False):
    _, seeds = data[0].split(":")
    seeds = [int(s) for s in seeds.split()]

    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    current = None

    for line in data[2:]:
        if line == "":
            current = None
        elif line == "seed-to-soil map:":
            current = seed_to_soil
        elif line == "soil-to-fertilizer map:":
            current = soil_to_fertilizer
        elif line == "fertilizer-to-water map:":
            current = fertilizer_to_water
        elif line == "water-to-light map:":
            current = water_to_light
        elif line == "light-to-temperature map:":
            current = light_to_temperature
        elif line == "temperature-to-humidity map:":
            current = temperature_to_humidity
        elif line == "humidity-to-location map:":
            current = humidity_to_location
        else:
            dst, src, sz = [int(n) for n in line.split()]
            assert current is not None
            current.append((dst, src, sz))

    maps_in_order = [
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location,
    ]

    locations = []
    for seed in seeds:
        i = seed
        print(i, end="")
        for t in maps_in_order:
            for m in t:
                if i >= m[1] and i < m[1] + m[2]:
                    i = m[0] + i - m[1]
                    break
            print(f" -> {i}", end="")
        locations.append(i)
        print()

    return min(locations)


def part2(data, verbose=False):
    _, seeds = data[0].split(":")
    seeds = [int(n) for n in seeds.split()]
    seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    current = None

    for line in data[2:]:
        if line == "":
            current = None
        elif line == "seed-to-soil map:":
            current = seed_to_soil
        elif line == "soil-to-fertilizer map:":
            current = soil_to_fertilizer
        elif line == "fertilizer-to-water map:":
            current = fertilizer_to_water
        elif line == "water-to-light map:":
            current = water_to_light
        elif line == "light-to-temperature map:":
            current = light_to_temperature
        elif line == "temperature-to-humidity map:":
            current = temperature_to_humidity
        elif line == "humidity-to-location map:":
            current = humidity_to_location
        else:
            dst, src, sz = [int(n) for n in line.split()]
            assert current is not None
            current.append((dst, src, sz))

    maps_in_order = [
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location,
    ]

    locations = []

    minloc = None
    loc = 0
    while True:
        if loc % 100000 == 0:
            print(loc)
        mloc = loc
        for t in reversed(maps_in_order):
            for m in t:
                dst, src, sz = m
                if mloc >= dst and mloc < dst + sz:
                    mloc = mloc - dst + src
                    break
        for r in seed_ranges:
            if mloc >= r[0] and mloc < r[1]:
                print(f"MIN LOC = {loc}")
                return loc
        loc += 1
    print("duh...")

    for seed_range in seed_ranges:
        for t in maps_in_order:
            for m in t:
                dst, src, sz = m
                if seed_range[0] < src + sz and seed_range[1] >= src:
                    seed_range = (
                        max(seed_range[0], m[1]),
                        min(seed_range[1], m[1] + m[2]),
                    )
                    seed_range = (
                        m[0] + seed_range[0] - m[1],
                        m[0] + seed_range[0] - m[1],
                    )

    # locations = []
    # for seed_range in seed_ranges:
    #     print(seed_range)
    #     seed = seed_range[0]

    #     while seed < seed_range[0] + seed_range[1]:
    #         i = seed
    #         # print(i, end="")
    #         for t in maps_in_order:
    #             for m in t:
    #                 if i >= m[1] and i < m[1] + m[2]:
    #                     i = m[0] + i - m[1]
    #                     break
    #             # print(f" -> {i}", end="")
    #         locations.append(i)
    #         seed += 1
    #         # print()

    return min(locations)


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
