Day 18
======

This day was a really tough one: at first I ran into problems getting example 4
and the puzzle input to solve in reasonable time. But most annoyingly, after
solving that, the solution for the puzzle input was too high. I spent way too long
time debugging this and seeking advice on the AoC Reddit, before I reread the
instruction for the 100th time: turns out I looked for the shortest path to visit
all keys and doors, while the task was to just visit *all keys*, not doors.

As I struggled with the exercise, I decided to retreat to Python, as I've more
experience with that language and so I can think about the problem with less
of a language overhead.

For Part 2, I consider all doors not having a key in the current quarter to
be open, solve all the four squares and use the sum of the shortest path
as answer.

The code for this day is nowhere near as clean as for most other days, and
I've still not implemented a solution in Go. I might come back to clean it
up later. Then again, maybe not...
