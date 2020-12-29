def transform(subject_number, loop_size):
    v = 1
    for i in range(loop_size):
        v = v * subject_number
        v = v % 20201227
    return v


def transform_until(subject_number, target):
    v = 1
    loops = 0
    while True:
        loops += 1
        v = v * subject_number
        v = v % 20201227
        if target == v:
            break
    return loops


# Example data:
card_public_key = 5764801
door_public_key = 17807724

# Input data:
card_public_key = 3469259
door_public_key = 13170438

card_loop_size = transform_until(7, card_public_key)
print(f"Card loop size: {card_loop_size}")

door_loop_size = transform_until(7, door_public_key)
print(f"Door loop size: {door_loop_size}")

print(f"Part 2: {transform(door_public_key, card_loop_size)}")