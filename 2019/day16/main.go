// Day 16 was challenging. The first part was not so bad,
// but the solution for part one was, while correct, not
// fast enough to solve the second part. This day was the
// first time I had to seek advice on Reddit for how to
// solve part two. The trick is that the output is placed
// at the end of the data, which means that we don't have
// to run the calculations for the entire data set. And
// the matrix is constructed so that we can cumulatively
// sum the values at the end of the data set in reverse
// until the offset is reached. I had to draw the matrix
// on a paper before I finally came to understand that:
// The lower, right quarter of the matrix is always a
// triangular like this:
//
// [ 1 1 1 1 ]
// [ 0 1 1 1 ]
// [ 0 0 1 1 ]
// [ 0 0 0 1 ]
//
// Given this, the code in runPhasePartTwo should be
// quite easy to understand.

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func runPhase(input []int) (output []int) {
	base := []int{0, 1, 0, -1}
	output = make([]int, len(input))
	for i := range input {
		n := 0
		for j := range input {
			a := base[((j+1)/(i+1))%4]
			n += input[j] * a
		}
		output[i] = abs(n) % 10
	}
	return output
}

// This was my first intent to optimize runPhase
// so that it would be fast enough for part two.
// While it is a bit faster, it's still nowhere
// near fast enough to solve the task in time.
func runPhase2(input []int) (output []int) {
	output = make([]int, len(input))

	// For each digit in the input ...
	var iter int
	for i := range input {
		n := 0
		iter = 0

		// Repeat the base line pattern
		for j := 0; j*(i+1)*4 < len(input); j++ {
			offs := j * (i + 1) * 4

			for k := 0; k < i+1; k++ {
				idx := offs + (i + 1) + k - 1
				if idx >= len(input) {
					break
				}
				n += input[idx]
			}

			for k := 0; k < i+1; k++ {
				idx := offs + (i+1)*3 + k - 1
				if idx >= len(input) {
					break
				}
				n -= input[idx]
				iter++
			}
		}

		output[i] = abs(n) % 10
	}
	return output
}

func runPhasePartTwo(offset int, input []int) (output []int) {
	output = make([]int, len(input))
	a := 0
	for i := len(input) - 1; i >= offset; i-- {
		a = a + input[i]
		output[i] = abs(a) % 10
	}
	return output
}

func repeat(src []int, count int) (result []int) {
	for i := 0; i < count; i++ {
		result = append(result, src...)
	}
	return
}

func parse(text string) (result []int) {
	trimmed := strings.TrimSpace(text)
	result = make([]int, len(trimmed))
	for i := range trimmed {
		result[i] = int(trimmed[i] - '0')
	}
	return result
}

func header(text string, line string) {
	fmt.Printf("\n%s\n%s\n", text, strings.Repeat(line, len(text)))
}

// TestCase should have comment.
type TestCase struct {
	name   string
	input  string
	expect []int
	phases int
}

func main() {
	var input []int

	content, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}

	header("Part One:", "=")

	partOneTests := []TestCase{
		{
			"Example 1:",
			"12345678",
			[]int{0, 1, 0, 2, 9, 4, 9, 8},
			4,
		},
		{
			"Example 2:",
			"80871224585914546619083218645595",
			[]int{2, 4, 1, 7, 6, 1, 7, 6},
			100,
		},
		{
			"Example 3:",
			"19617804207202209144916044189917",
			[]int{7, 3, 7, 4, 5, 4, 1, 8},
			100,
		},
		{
			"Example 4:",
			"69317163492948606335995924319873",
			[]int{5, 2, 4, 3, 2, 1, 3, 3},
			100,
		},
		{
			"With puzzle input:",
			string(content),
			[]int{},
			100,
		},
	}

	for _, test := range partOneTests {
		header(test.name, "-")
		input = parse(test.input)
		for i := 0; i < test.phases; i++ {
			input = runPhase2(input)
			if test.phases < 100 {
				fmt.Printf("Phase %d:   %v\n", i+1, input)
			}
		}
		if test.phases >= 100 {
			fmt.Printf("Phase %d: %v\n", test.phases, input[:8])
		}
		if len(test.expect) > 0 {
			fmt.Printf("Expected:  %v\n", test.expect)
		}
	}

	fmt.Println()
	header("Part Two:", "=")

	partTwoTests := []TestCase{
		{
			"Example 1:",
			"03036732577212944063491565474664",
			[]int{8, 4, 4, 6, 2, 0, 2, 6},
			100,
		},
		{
			"Example 2:",
			"02935109699940807407585447034323",
			[]int{7, 8, 7, 2, 5, 2, 7, 0},
			100,
		},
		{
			"Example 3:",
			"03081770884921959731165446850517",
			[]int{5, 3, 5, 5, 3, 7, 3, 1},
			100,
		},
		{
			"With puzzle input:",
			string(content),
			[]int{},
			100,
		},
	}

	for _, test := range partTwoTests {
		header(test.name, "-")
		input = repeat(parse(test.input), 10000)
		offset, err := strconv.Atoi(test.input[:7])
		if err != nil {
			log.Fatal(err)
		}
		for i := 0; i < test.phases; i++ {
			input = runPhasePartTwo(offset, input)
		}
		result := input[offset : offset+8]
		fmt.Printf("Phase %d at offset %d: %v\n", test.phases, offset, result)
		if len(test.expect) > 0 {
			fmt.Printf("Expected: %v\n", test.expect)
		}
	}

	fmt.Println("\nDone!")
}
