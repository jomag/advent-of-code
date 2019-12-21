package main

import (
	"fmt"
	"strings"
)

func isPath(c byte) bool {
	return c == '#' || c == '|' || c == '-' || c == 'O' || c == '+' || c == '>' || c == '<' || c == '^' || c == 'v'
}

func prettify(canvas *Canvas) int {
	sum := 0

	for y := 0; y < canvas.height; y++ {
		for x := 0; x < canvas.width; x++ {
			if canvas.Get(x, y) == '.' {
				canvas.Set(x, y, ' ')
			}

			if canvas.Get(x, y) == '#' {
				n := isPath(canvas.Get(x, y-1))
				s := isPath(canvas.Get(x, y+1))
				w := isPath(canvas.Get(x-1, y))
				e := isPath(canvas.Get(x+1, y))
				var count int
				for _, val := range []bool{n, s, w, e} {
					if val {
						count++
					}
				}

				if count == 4 {
					canvas.Set(x, y, '+')
					sum += x * y
				} else if count == 3 {
					canvas.Set(x, y, '+')
				} else if count == 2 {
					if n && s {
						canvas.Set(x, y, '|')
					} else if w && e {
						canvas.Set(x, y, '-')
					} else {
						canvas.Set(x, y, '+')
					}
				} else {
					if n || s {
						canvas.Set(x, y, '|')
					} else {
						canvas.Set(x, y, '-')
					}
				}
			}
		}
	}

	return sum
}

func partOne() {
	var m IntCodeMachine
	m.Init([]int{}, []int{})
	m.Load("input.txt")
	m.Run([]int{})
	output := m.ReadOutput()
	img := make([]byte, len(output))
	for i := 0; i < len(output); i++ {
		img[i] = byte(output[i])
	}

	canvas := NewCanvasFromString(string(img))
	sum := prettify(canvas)

	canvas.Render([]Sprite{}, false)
	fmt.Printf("%d rows, %d columns\n", canvas.width, canvas.height)
	fmt.Printf("Sum of alignment parameters: %d\n", sum)
}

func partTwo() {
	mainRoutine := "A,B,A,C,B,C,B,A,C,B\n"
	functionA := "L,6,R,8,R,12,L,6,L,8\n"
	functionB := "L,10,L,8,R,12\n"
	functionC := "L,8,L,10,L,6,L,6\n"
	videoFeed := "y\n"
	combined := mainRoutine + functionA + functionB + functionC + videoFeed

	commands := make([]int, len(combined))
	for i, b := range []byte(combined) {
		commands[i] = int(b)
	}

	var m IntCodeMachine
	m.Init([]int{}, []int{})
	m.Load("input.txt")
	m.memory[0] = 2
	m.Run(commands)
	output := m.ReadOutput()
	img := make([]byte, len(output))
	for i := 0; i < len(output); i++ {
		img[i] = byte(output[i])
	}

	frames := strings.Split(string(img), "\n\n")

	// Clear screen
	fmt.Println("\033c")

	for _, frame := range frames {
		if strings.Count(frame, "\n") == 36 {
			canvas := NewCanvasFromString(frame)
			prettify(canvas)
			canvas.Render([]Sprite{}, true)
			fmt.Scanln()
		} else {
			fmt.Println("\033c")
			fmt.Println(frame)
			fmt.Scanln()
		}
	}

	fmt.Printf("Final output: %d", output[len(output)-1])
}

func main() {
	partOne()
	fmt.Println("Press enter key to continue with part two...")
	fmt.Scanln()
	partTwo()
}
