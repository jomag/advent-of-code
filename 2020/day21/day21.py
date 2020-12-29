import sys, re

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
with open(filename) as f:
    lines = f.readlines()

# Contains list of foods (list of ingredients) with allergen as key
foods = {}
all_ingredients = set()
ingredient_count = {}

for line in lines:
    m = re.match("([a-z ]+)\\(contains ([ ,a-z]+)\\)", line)
    assert m
    ingredients = set(m.group(1).strip().split())
    all_ingredients.update(ingredients)
    allergens = [a.strip() for a in m.group(2).split(",")]
    for a in allergens:
        if a in foods.keys():
            foods[a].append(ingredients)
        else:
            foods[a] = [ingredients]
    for i in ingredients:
        if i in ingredient_count:
            ingredient_count[i] += 1
        else:
            ingredient_count[i] = 1

x = set()
for a, f in foods.items():
    isect = set.intersection(*f)
    x.update(isect)

na = all_ingredients.difference(x)
part1 = sum(ingredient_count[a] for a in na)
print(f"Part 1: {part1}")

#### Part 2

x = {}

for a, f in foods.items():
    isect = set.intersection(*f)
    x[a] = isect

transl = {}

while True:
    for a, f in x.items():
        if len(f) == 1:
            i = f.pop()
            transl[a] = i
            x = {k: v.difference(set([i])) for k, v in x.items()}
            break
    else:
        break

print("Part 2: " + ",".join([transl[a] for a in sorted(transl.keys())]))
