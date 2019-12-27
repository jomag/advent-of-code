// My initial attempt to solve part two was to find the distance where
// the two lines in the beam intersected upper right and lower left
// corner of the 100x100 square. While it did mostly work, I got some
// problems with rounding differences between my code and the IntCode
// implementation, so I opted for a simpler solution instead that steps
// through each row and tests if the beam will fit the entire square with
// the lower left corner placed where the closest '#' is. It would
// fail if the beam was pointing more to the right than downward, but that
// was not the case with my input and it would be simple to adapt the algo.
// It takes 4 seconds to brute force it like this on my computer.

package main

import "fmt"

func partOne(m *IntCodeMachine) {
	width := 50
	height := 50
	canvas := NewCanvas(width, height, true, '.')
	count := 0
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			m.Reset()
			m.Run([]int{x, y})
			out := m.ReadOutput()
			if out[0] == 1 {
				canvas.Set(x, y, '#')
				count++
			}
		}
	}

	canvas.Render([]Sprite{}, false)
	fmt.Printf("Result: %d\n", count)
}

func partTwo(m *IntCodeMachine) {
	test := func(x, y int) bool {
		for cy := 0; cy < 100; cy++ {
			for cx := 0; cx < 100; cx++ {
				m.Reset()
				m.Run([]int{cx + x, cy + y})
				out := m.ReadOutput()
				if out[0] != 1 {
					return false
				}
			}
		}
		return true
	}

	y := 150
	for {
		x := 0
		for {
			m.Reset()
			m.Run([]int{x + 1, y})
			out := m.ReadOutput()
			if out[0] != 0 {
				break
			}
			x++
		}

		if test(x, y-100) {
			fmt.Printf("x=%d, y=%d => %d\n", x, y-100, x*10000+y)
			break
		}

		y++
	}
}

func main() {
	var m IntCodeMachine
	m.Load("input.txt")

	fmt.Printf("Part One\n========\n\n")
	partOne(&m)

	fmt.Printf("\nPart Two\n========\n\n")
	partTwo(&m)
}
