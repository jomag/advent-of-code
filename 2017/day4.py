
def validate_no_duplicate_words(pwd):
    found = set()
    words = pwd.split()
    for w in words:
        if w in found:
            return False
        found.add(w)
    return True


def validate_no_anagrams(pwd):
    found = set()
    words = pwd.split()
    for w in words:
        ww = "".join(sorted(w))
        if ww in found:
            return False
        found.add(ww)
    return True


assert validate_no_duplicate_words("aa bb cc dd ee")
assert not validate_no_duplicate_words("aa bb cc dd aa")
assert validate_no_duplicate_words("aa bb cc dd aaa")

assert validate_no_anagrams("abcde fghij")
assert not validate_no_anagrams("abcde xyz ecdab")
assert validate_no_anagrams("a ab abc abd abf abj")
assert validate_no_anagrams("iiii oiii ooii oooi oooo")
assert not validate_no_anagrams("oiii ioii iioi iiio")

with open("day4.txt") as f:
    data = f.read()

print(sum(1 for p in data.splitlines() if validate_no_duplicate_words(p)))
print(sum(1 for p in data.splitlines() if validate_no_anagrams(p)))

