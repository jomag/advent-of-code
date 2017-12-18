
class Parser:
    def parse(self, txt):
        self.txt = str(txt)
        self.pos = 0
        return self._parse_group()

    def peek(self):
        return self.txt[self.pos]

    def pop(self):
        c = self.txt[self.pos]
        self.pos += 1
        return c

    def _skip_escapes(self):
        while self.peek() == "!":
            self.pop()
            self.pop()

    def _parse_child(self):
        c = self.peek()
        if c == "{":
            return self._parse_group()
        elif c == "<":
            return self._parse_garbage()
        else:
            raise RuntimeError("Expected start of new group or garbage")

    def _parse_garbage(self):
        assert self.pop() == "<"
        garbage = ""
        while True:
            self._skip_escapes()
            c = self.peek()
            if c == ">":
                self.pop()
                return garbage
            else:
                garbage += self.pop()

    def _parse_group(self):
        assert self.pop() == "{"
        grp = []
        while True:
            self._skip_escapes()
            c = self.peek()

            if c == "}":
                self.pop()
                return grp
            else:
                grp.append(self._parse_child())

            self._skip_escapes()
            c = self.peek()
            if c == "}":
                self.pop()
                return grp
            elif c == ",":
                self.pop()
            else:
                raise RuntimeError("Expected end of group or new child")


def calculate_score(grp, score=1):
    return score + sum(calculate_score(child, score+1) for child in grp if type(child) is list)


def count_garbage(grp):
    return sum(count_garbage(c) for c in grp if type(c) is list) + \
           sum(len(c) for c in grp if type(c) is str)


parser = Parser()

result = parser.parse("{}")
assert result == []
assert calculate_score(result) == 1

result = parser.parse("{{{}}}")
assert result == [[[]]]
assert calculate_score(result) == 6

result = parser.parse("{{},{}}")
assert result == [[], []]
assert calculate_score(result) == 5

result = parser.parse("{{{},{},{{}}}}")
assert result == [[[], [], [[]]]]
assert calculate_score(result) == 16

result = parser.parse("{<{},{},{{}}>}")
assert result == ["{},{},{{}}"]

result = parser.parse("{<a>,<a>,<a>,<a>}")
assert result == ["a", "a", "a", "a"]
assert calculate_score(result) == 1

result = parser.parse("{{<a>},{<a>},{<a>},{<a>}}")
assert result == [["a"], ["a"], ["a"], ["a"]]
assert calculate_score(result) == 9

result = parser.parse("{{<!!>},{<!!>},{<!!>},{<!!>}}")
assert result == [[""], [""], [""], [""]]
assert calculate_score(result) == 9

result = parser.parse("{{<!>},{<!>},{<!>},{<a>}}")
assert result == [["},{<},{<},{<a"]]

result = parser.parse("{{<a!>},{<a!>},{<a!>},{<ab>}}")
assert calculate_score(result) == 3

result = parser.parse("{<>}")
assert count_garbage(result) == 0

result = parser.parse("{<random characters>}")
assert count_garbage(result) == 17

result = parser.parse("{<<<<>}")
assert count_garbage(result) == 3

result = parser.parse("{<{!>}>}")
assert count_garbage(result) == 2

result = parser.parse("{<!!>}")
assert count_garbage(result) == 0

result = parser.parse("{<!!!>>}")
assert count_garbage(result) == 0

result = parser.parse("{<{o\"i!a,<{i<a>}")
assert count_garbage(result) == 10

with open("day9.txt") as f:
    input_data = f.read()

result = parser.parse(input_data)
print(calculate_score(result))
print(count_garbage(result))
