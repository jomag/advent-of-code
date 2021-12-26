from typing import List, Optional


def cost_per_step(pod):
    return {"a": 1, "b": 10, "c": 100, "d": 1000}[pod]


class Board:
    state: List[str]

    def __init__(self, rooms=None):
        state = ["." for _ in range(11 + 4 * 4)]

        if rooms:
            state[11] = rooms[0][0]
            state[12] = rooms[0][1]
            state[13] = rooms[0][2]
            state[14] = rooms[0][3]

            state[15] = rooms[1][0]
            state[16] = rooms[1][1]
            state[17] = rooms[1][2]
            state[18] = rooms[1][3]

            state[19] = rooms[2][0]
            state[20] = rooms[2][1]
            state[21] = rooms[2][2]
            state[22] = rooms[2][3]

            state[23] = rooms[3][0]
            state[24] = rooms[3][1]
            state[25] = rooms[3][2]
            state[26] = rooms[3][3]

        self.state = state

    def print(self):
        print("#" * 13)
        print("#" + "".join(self.at("h", n) for n in range(11)) + "#")
        print("###" + "#".join(self.at(r, 0) for r in ["a", "b", "c", "d"]) + "###")
        print("  #" + "#".join(self.at(r, 1) for r in ["a", "b", "c", "d"]) + "#")
        print("  #" + "#".join(self.at(r, 2) for r in ["a", "b", "c", "d"]) + "#")
        print("  #" + "#".join(self.at(r, 3) for r in ["a", "b", "c", "d"]) + "#")
        print("  " + "#" * 9)
        print()

    def copy(self):
        b = Board()
        b.state = [x for x in self.state]
        return b

    def move(self, start, end):
        c = self.copy()
        pod = c.at(start)
        c.set(pod, end)
        c.set(".", start)

        if not c.validate():
            print("Before: ")
            self.print()
            print("After: ")
            c.print()
            raise Exception("Unhandled case: empty spot inside room")

        return c

    def is_done(self):
        return all(self.at(r, n) == r for r in ["a", "b", "c", "d"] for n in [0, 1])

    def to_index(self, r: str, n: Optional[int] = None):
        if n is None:
            r, n = r[0], int(r[1:])
        assert n >= 0 and n < 11
        if r == "h":
            return n
        assert n < 4
        if r == "a":
            return 11 + n
        if r == "b":
            return 15 + n
        if r == "c":
            return 19 + n
        if r == "d":
            return 23 + n
        raise Exception(f"Invalid position: {r} {n}")

    def set(self, pod: str, r: str, n: Optional[int] = None):
        idx = self.to_index(r, n)
        assert (
            self.state[idx] == "." or pod == "."
        ), f"set({pod}, {r}, {n}): move {pod} to room with {self.state[idx]} (idx: {idx})"
        self.state[idx] = pod

    def at(self, r: str, n: Optional[int] = None):
        return self.state[self.to_index(r, n)]

    def possible_moves_from_hallway(self):
        moves = []

        for x in range(11):
            pod = self.at("h", x)
            if pod == ".":
                continue

            # Test if the target room is occupied by other pod types
            if any(self.at(pod, n) not in (".", pod) for n in range(4)):
                continue

            entrance = {"a": 2, "b": 4, "c": 6, "d": 8}[pod]

            step = 1 if entrance > x else -1
            if all(self.at("h", i) == "." for i in range(x + step, entrance, step)):
                for n in range(3, -1, -1):
                    if self.at(pod, n) == ".":
                        moves.append(
                            (
                                f"h{x}",
                                f"{pod}{n}",
                                (n + 1 + abs(x - entrance)) * cost_per_step(pod),
                            )
                        )
                        break

        return moves

    def validate(self):
        for room in ["a", "b", "c", "d"]:
            empty = True
            for n in range(4):
                if self.at(room, n) == ".":
                    if not empty:
                        self.print()
                        return False
                else:
                    empty = False
        return True

    def room_contains_only_correct_pod(self, room):
        return all(self.at(room, i) == room for i in range(4))

    def possible_moves_from_room(self, room):
        moves = []

        # This room is empty. No moves start here.
        if all(self.at(room, i) == "." for i in range(4)):
            return []

        # Room is filled with correct pod. Done!
        if all(self.at(room, i) == room for i in range(4)):
            return []

        entrances = {"a": 2, "b": 4, "c": 6, "d": 8}

        def test_hallway(start_pos, pod, x, cost):
            nonlocal moves
            if x == entrances[pod]:
                start_x = entrances[start_pos[0]]
                horz_cost = cost_per_step(pod) * abs(start_x - x)
                if self.room_contains_only_correct_pod(pod):
                    for i in range(3, -1, -1):
                        if self.at(room, i) == ".":
                            moves.append(
                                (
                                    start_pos,
                                    f"{pod}{i}",
                                    cost + horz_cost + cost_per_step(pod) * (i + 1),
                                )
                            )

            if x not in [2, 4, 6, 8]:
                start_x = entrances[start_pos[0]]
                moves.append(
                    (start_pos, f"h{x}", cost + cost_per_step(pod) * abs(start_x - x))
                )

        # Test moves from the each cell in the current room
        for i in range(4):
            p = self.at(f"{room}{i}")
            if p != ".":
                for x in range(entrances[room], -1, -1):
                    if self.at("h", x) != ".":
                        break
                    test_hallway(f"{room}{i}", p, x, (i + 1) * cost_per_step(p))

                for x in range(entrances[room], 11):
                    if self.at("h", x) != ".":
                        break
                    test_hallway(f"{room}{i}", p, x, (i + 1) * cost_per_step(p))
                break

        return moves

    def possible_moves(self):
        return (
            self.possible_moves_from_room("a")
            + self.possible_moves_from_room("b")
            + self.possible_moves_from_room("c")
            + self.possible_moves_from_room("d")
            + self.possible_moves_from_hallway()
        )


def part1(rooms, verbose=False):
    brd = Board(rooms)
    min_cost = None
    best_path = []
    visited_states = {}
    attempt = 0

    def print_verbose_state(brd):
        print("Board:")
        brd.print()
        print("Moves from room A: ", brd.possible_moves_from_room("a"))
        print("Moves from room B: ", brd.possible_moves_from_room("b"))
        print("Moves from room C: ", brd.possible_moves_from_room("c"))
        print("Moves from room D: ", brd.possible_moves_from_room("d"))
        print("Moves from hallway: ", brd.possible_moves_from_hallway())

    def rec(brd: Board, cost: int, path: List):
        nonlocal verbose, attempt
        nonlocal min_cost, best_path

        attempt += 1
        if attempt % 100000 == 0:
            print(f"Attempt {attempt}")

        if min_cost is not None and min_cost < cost:
            return

        investigate = [("d0", "h10"), ("d1", "h0")]
        state_tuple = tuple(brd.state)

        if len(path) > 0 and all(
            investigate[n][0] == path[n][0] and investigate[n][1] == path[n][1]
            for n in range(min(len(investigate), len(path)))
        ):
            print("WHUTT!!")
            print(path)
            print_verbose_state(brd)
            print(f"Already visited? {state_tuple in visited_states}")
            # input()

        if state_tuple in visited_states:
            if visited_states[state_tuple] <= cost:
                return
        visited_states[state_tuple] = cost

        if verbose:
            print_verbose_state(brd)
            input()

        if brd.is_done():
            if min_cost is None or min_cost > cost:
                best_path = path
                min_cost = cost
                print(f"New min cost: {min_cost}")
        else:
            moves = brd.possible_moves()
            for move in moves:
                npath = [p for p in path] + [move]
                new_board = brd.move(move[0], move[1])

                # if all(
                #     investigate[n][0] == npath[n][0]
                #     and investigate[n][1] == npath[n][1]
                #     for n in range(len(npath))
                # ):
                #     # verbose = True
                #     print(f"Found! {npath}")
                #     print(f"Cost: {cost + move[2]}")
                #     # new_board.print()
                #     print_verbose_state(new_board)

                # if len(investigate) == len(npath):
                #     if all(
                #         investigate[n][0] == npath[n][0]
                #         and investigate[n][1] == npath[n][1]
                #         for n in range(len(investigate))
                #     ):
                #         verbose = True
                #         print(f"Found! {npath}")

                rec(new_board, cost + move[2], npath)

    rec(brd, 0, [])

    if min_cost is None:
        print("No solution found")
    else:
        print("Lowest cost: ", min_cost)
        print("Best moves: ", best_path)

        if verbose:
            c = brd.copy()
            c.print()
            cost = 0
            for move in best_path:
                c = c.move(move[0], move[1])
                print(f"Move from {move[0]} to {move[1]}")
                cost = cost + move[2]
                print(f"Cost: {move[2]}. Total cost: {cost}")
                c.print()
                input()

    return 1


example = [["b", "a"], ["c", "d"], ["b", "c"], ["d", "a"]]
inp = [["d", "d"], ["a", "c"], ["c", "b"], ["a", "b"]]
example2 = [
    ["b", "d", "d", "a"],
    ["c", "c", "b", "d"],
    ["b", "b", "a", "c"],
    ["d", "a", "c", "a"],
]
example3 = [
    ["b", "a", "a", "a"],
    ["a", "b", "b", "b"],
    ["c", "c", "c", "c"],
    ["d", "d", "d", "d"],
]
inp2 = [
    ["d", "d", "d", "d"],
    ["a", "c", "b", "c"],
    ["c", "b", "a", "b"],
    ["a", "a", "c", "b"],
]

import sys

sys.setrecursionlimit(10000)
print(f"Part 1 with example data: {part1(inp2, verbose=False)}")
# print(f"Part 1 with real input: {part1(lines)}")
# print(f"Part 2 with example data: {part2(example, verbose=True)}")
# print(f"Part 2 with real input: {part2(lines)}")
