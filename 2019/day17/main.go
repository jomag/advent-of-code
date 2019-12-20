package main

import (
	"fmt"
)

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

	sum := 0
	for y := 1; y < canvas.height-1; y++ {
		for x := 1; x < canvas.width-1; x++ {
			if canvas.Get(x, y) == '#' {
				n := canvas.Get(x, y-1)
				s := canvas.Get(x, y+1)
				w := canvas.Get(x-1, y)
				e := canvas.Get(x+1, y)
				if n == '#' && s == '#' && w == '#' && e == '#' {
					canvas.Set(x, y, 'O')
					sum += x * y
				}
			}
		}
	}

	canvas.Render([]Sprite{})
	fmt.Printf("%d rows, %d columns\n", canvas.width, canvas.height)
	fmt.Printf("Sum of alignment parameters: %d\n", sum)
}

func main() {
	partOne()
}
