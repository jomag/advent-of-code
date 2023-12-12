from functools import cmp_to_key


def parse_hand_part1(h):
    values = list(
        reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])
    )
    assert len(h) == 5, "Hand is not five cards!"
    return [values.index(c) for c in h]


def parse_hand_part2(h):
    values = list(
        reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"])
    )
    assert len(h) == 5, "Hand is not five cards!"
    return [values.index(c) for c in h]


def get_card_count_by_value(hand):
    cnt = {}
    for c in hand:
        try:
            cnt[c] += 1
        except KeyError:
            cnt[c] = 1
    return cnt


def is_five_of_a_kind_p1(hand):
    return 5 in get_card_count_by_value(hand).values()


def is_five_of_a_kind_p2(hand):
    jc = hand.count(0)
    h2 = [c for c in hand if c != 0]
    return all(h2[0] == c for c in h2)


def is_four_of_a_kind_p1(hand):
    return 4 in get_card_count_by_value(hand).values()


def is_four_of_a_kind_p2(hand):
    jc = hand.count(0)
    if jc >= 3:
        return True
    if jc == 2:
        return is_two_pair_p1(hand)
    if jc == 1:
        return is_three_of_a_kind_p1(hand)
    return is_four_of_a_kind_p1(hand)


def is_full_house_p1(hand):
    c = get_card_count_by_value(hand).values()
    return 3 in c and 2 in c


def is_full_house_p2(hand):
    jc = hand.count(0)
    if jc == 5 or jc == 4 or jc == 3:
        return True
    if jc == 2 or jc == 1:
        return is_two_pair_p1(hand)
    return is_full_house_p1(hand)


def is_three_of_a_kind_p1(hand):
    return 3 in get_card_count_by_value(hand).values()


def is_three_of_a_kind_p2(hand):
    jc = hand.count(0)
    if jc >= 2:
        return True
    if jc == 1:
        return is_one_pair_p1(hand)
    return is_three_of_a_kind_p1(hand)


def is_two_pair_p1(hand):
    cnt = get_card_count_by_value(hand).values()
    return len([c for c in cnt if c == 2]) == 2


def is_two_pair_p2(hand):
    jc = hand.count(0)
    if jc >= 2:
        return True
    if jc >= 1:
        return is_one_pair_p1(hand)
    return is_two_pair_p1(hand)


def is_one_pair_p1(hand):
    return 2 in get_card_count_by_value(hand).values()


def is_one_pair_p2(hand):
    jc = hand.count(0)
    if jc > 0:
        return True
    return 2 in get_card_count_by_value(hand).values()


def is_high_card_p1(hand):
    return len(set(hand)) == len(hand)


def is_high_card_p2(hand):
    h2 = [c for c in hand if c != 0]
    return len(set(h2)) == len(h2)


def get_hand_type_value_p1(h):
    if is_five_of_a_kind_p1(h):
        return 7
    if is_four_of_a_kind_p1(h):
        return 6
    if is_full_house_p1(h):
        return 5
    if is_three_of_a_kind_p1(h):
        return 4
    if is_two_pair_p1(h):
        return 3
    if is_one_pair_p1(h):
        return 2
    if is_high_card_p1(h):
        return 1
    return 0


def get_hand_type_value_p2(h):
    if is_five_of_a_kind_p2(h):
        return 7
    if is_four_of_a_kind_p2(h):
        return 6
    if is_full_house_p2(h):
        return 5
    if is_three_of_a_kind_p2(h):
        return 4
    if is_two_pair_p2(h):
        return 3
    if is_one_pair_p2(h):
        return 2
    if is_high_card_p2(h):
        return 1
    return 0


def compare_bids_p1(a, b):
    va = get_hand_type_value_p1(a[0])
    vb = get_hand_type_value_p1(b[0])
    if va < vb:
        return -1
    if va > vb:
        return +1
    for n in range(5):
        if a[0][n] < b[0][n]:
            return -1
        if a[0][n] > b[0][n]:
            return 1
    return 0


def compare_bids_p2(a, b):
    va = get_hand_type_value_p2(a[0])
    vb = get_hand_type_value_p2(b[0])
    if va < vb:
        return -1
    if va > vb:
        return +1
    for n in range(5):
        if a[0][n] < b[0][n]:
            return -1
        if a[0][n] > b[0][n]:
            return 1
    return 0


def part1(data, verbose=False):
    bids = []
    for line in data:
        hand, bid = line.split()
        bids.append((parse_hand_part1(hand), int(bid)))

    bids.sort(key=cmp_to_key(compare_bids_p1))
    print(bids)

    tot = 0
    for n in range(len(bids)):
        tot += bids[n][1] * (n + 1)

    return tot


def part2(data, verbose=False):
    bids = []
    for line in data:
        hand, bid = line.split()
        bids.append((parse_hand_part2(hand), int(bid)))

    bids.sort(key=cmp_to_key(compare_bids_p2))
    print(bids)

    tot = 0
    for n in range(len(bids)):
        tot += bids[n][1] * (n + 1)

    return tot


with open("input.txt") as f:
    lines = [ln.strip() for ln in f.readlines()]

with open("example.txt") as f:
    example = [ln.strip() for ln in f.readlines()]

# print(f"Part 1 with example data: {part1(example, verbose=True)}")
# print(f"Part 1 with real input: {part1(lines)}")
print(f"Part 2 with example data: {part2(example, verbose=True)}")
print(f"Part 2 with real input: {part2(lines)}")
