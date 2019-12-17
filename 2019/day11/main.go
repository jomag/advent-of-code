package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

const nocolor = " "
const black = "."
const white = "#"

// State - current state
type State struct {
	step   int
	width  int
	height int
	canvas [][]string
	x      int
	y      int
	dir    byte
	count  int
}

func createState(width, height int, color string) (state *State) {
	state = new(State)
	state.step = 0
	state.width = width
	state.height = height
	state.x = width / 2
	state.y = height / 2
	state.dir = 'U'

	state.canvas = make([][]string, height)
	for i := range state.canvas {
		state.canvas[i] = make([]string, width)
		for j := range state.canvas[i] {
			state.canvas[i][j] = color
		}
	}

	return
}

func (state *State) render() {
	label := fmt.Sprintf("[Step %d]", state.step)
	fmt.Printf("\n+--%s%s+\n", label, strings.Repeat("-", state.width-2-len(label)))
	for y := 0; y < state.height; y++ {
		if y == state.y {
			str := "|"
			for x := 0; x < state.width; x++ {
				if x == state.x {
					str += "R"
				} else {
					str += state.canvas[y][x]
				}
			}
			fmt.Println(str + "|")
		} else {
			fmt.Println("|" + strings.Join(state.canvas[y], "") + "|")
		}
	}
	fmt.Println("+" + strings.Repeat("-", state.width) + "+")
}

func readInput(filename string) (string, error) {
	raw, err := ioutil.ReadFile(filename)
	if err != nil {
		return "", err
	}
	return string(raw), nil
}

func run(prg []int, state *State) {
	var m IntCodeMachine
	m.Init(prg, []int{})
	for {
		var color int

		switch state.canvas[state.y][state.x] {
		case white:
			color = 1
		case black:
			color = 0
		case nocolor:
			color = 0
		}

		err := m.Run([]int{color})
		if err != nil {
			log.Fatal(err)
		}

		if m.stopped {
			break
		}

		output := m.ReadOutput()
		if len(output) != 2 {
			log.Fatal("Expected 2 output value")
		}

		// First output is color to paint
		var paintColor string
		switch output[0] {
		case 0:
			paintColor = black
		case 1:
			paintColor = white
		default:
			log.Fatalf("Invalid color: %d", output[0])
		}

		switch output[1] {
		case 0:
			// Turn left 90 degrees
			switch state.dir {
			case 'U':
				state.dir = 'L'
			case 'L':
				state.dir = 'D'
			case 'D':
				state.dir = 'R'
			case 'R':
				state.dir = 'U'
			}
		case 1:
			// Turn right 90 degrees
			switch state.dir {
			case 'U':
				state.dir = 'R'
			case 'R':
				state.dir = 'D'
			case 'D':
				state.dir = 'L'
			case 'L':
				state.dir = 'U'
			}
		default:
			log.Fatalf("Illegal turn: %d", output[1])
		}

		if state.canvas[state.y][state.x] == nocolor {
			state.count++
		}

		state.canvas[state.y][state.x] = paintColor

		switch state.dir {
		case 'U':
			state.y--
		case 'L':
			state.x--
		case 'D':
			state.y++
		case 'R':
			state.x++
		}

		state.step++

		//state.render()
		//fmt.Scanln()
	}
}

func main() {
	src, err := readInput("input.txt")
	if err != nil {
		log.Fatal(err)
	}

	prg, err := Parse(src)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Part One:")
	state := createState(120, 60, nocolor)
	run(prg, state)
	state.render()
	fmt.Printf("Count: %d\n", state.count)
	fmt.Println("Done!")

	fmt.Println("Part Two:")
	state = createState(120, 60, nocolor)
	state.canvas[state.y][state.x] = white
	run(prg, state)
	state.render()
	fmt.Printf("Count: %d\n", state.count)
	fmt.Println("Done!")
}
