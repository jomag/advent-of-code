import re


def validate_part1(batch):
    required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    optional = ["cid"]
    keys = batch.keys()
    required_found = [key for key in keys if key in required]
    optional_found = [key for key in keys if key in optional]
    if " ".join(sorted(required)) != " ".join(sorted(required_found)):
        return False

    return len(optional_found) + len(required_found) == len(keys)


def validate_part2(batch):
    if not validate_part1(batch):
        return False

    for k, v in batch.items():
        if k in ["byr", "iyr", "eyr"]:
            if not re.match(r"^\d\d\d\d$", v):
                return False

        if k == "byr" and (int(v) < 1920 or int(v) > 2002):
            return False
        if k == "iyr" and (int(v) < 2010 or int(v) > 2020):
            return False
        if k == "eyr" and (int(v) < 2020 or int(v) > 2030):
            return False

        if k == "hgt":
            unit = v[-2:]
            if unit not in ("cm", "in"):
                return False
            n = int(v[:-2])
            if unit == "cm" and (n < 150 or n > 193):
                return False
            if unit == "in" and (n < 59 or n > 76):
                return False

        if k == "hcl" and not re.match(r"^#[0-9a-f]{6}$", v):
            return False

        if k == "ecl" and v not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return False

        if k == "pid" and not re.match(r"^\d{9}$", v):
            return False

    return True


with open("input") as f:
    lines = [l.strip() for l in f.readlines()]

batches = []
batch = []

for line in lines:
    if len(line) == 0:
        batches.append(batch)
        batch = []
    else:
        batch.append(line)

batches.append(batch)

batches = [" ".join(lines) for lines in batches]
batches = [batch.split(" ") for batch in batches]
batches = [{item.split(":")[0]: item.split(":")[1] for item in b} for b in batches]

valid_count = sum(1 for batch in batches if validate_part1(batch))
print(f"Part 1: {valid_count}")

valid_count = sum(1 for batch in batches if validate_part2(batch))
print(f"Part 2: {valid_count}")
