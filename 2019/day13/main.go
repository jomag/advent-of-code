package main

import (
	"fmt"
	"log"
)

// State - game state
type State struct {
	width   int
	height  int
	canvas  []byte
	score   int
	ballX   int
	paddleX int
}

func newState(width, height int) (state *State) {
	state = new(State)
	state.width = width
	state.height = height
	state.canvas = make([]byte, (width+1)*height)
	for i := range state.canvas {
		if (i+1)%(width+1) == 0 {
			state.canvas[i] = '\n'
		} else {
			state.canvas[i] = '.'
		}
	}
	return
}

func (state *State) render() {
	fmt.Printf("Score: %d\n", state.score)
	fmt.Print(string(state.canvas))
}

func (state *State) countTiles(b byte) (count int) {
	for i := range state.canvas {
		if state.canvas[i] == b {
			count++
		}
	}
	return
}

func (state *State) setTile(x, y, n int) {
	p := (y+2)*(state.width+1) + x + 5
	switch n {
	case 0:
		state.canvas[p] = ' '
	case 1:
		state.canvas[p] = 'W'
	case 2:
		state.canvas[p] = 'B'
	case 3:
		state.canvas[p] = '-'
		state.paddleX = x
	case 4:
		state.canvas[p] = 'o'
		state.ballX = x
	}
}

func run(joystick int, m *IntCodeMachine, state *State) error {
	input := []int{}

	if joystick >= -1 && joystick <= 1 {
		input = []int{joystick}
	}

	err := m.Run(input)

	if err != nil {
		return err
	}

	output := m.ReadOutput()

	for i := 0; i < len(output); i += 3 {
		x := output[i]
		y := output[i+1]
		c := output[i+2]
		if x == -1 && y == 0 {
			state.score = c
		} else {
			state.setTile(x, y, c)
		}
	}

	state.render()
	return nil
}

func main() {
	var m IntCodeMachine
	err := m.Load("input.txt")

	state := newState(50, 24)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Print("Part One:\n\n")

	run(99, &m, state)
	blocks := state.countTiles('B')
	fmt.Printf("Blocks: %d\n", blocks)
	fmt.Print("Press enter to continue...")
	fmt.Scanln()

	fmt.Print("\n\nPart Two:\n\n")

	// Set memory address 0 to 2 for free plays
	m.Reset()
	m.memory[0] = 2
	var joystick int

	for {
		switch {
		case state.ballX > state.paddleX:
			joystick = 1
		case state.ballX < state.paddleX:
			joystick = -1
		default:
			joystick = 0
		}

		run(joystick, &m, state)
		// fmt.Scanln()
	}
}
