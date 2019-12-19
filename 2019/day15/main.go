package main

import (
	"fmt"
	"log"
	"math/rand"
	"time"
)

// State - current state
type State struct {
	x int
	y int
}

// Direction - relative direction
type Direction struct {
	dx int
	dy int
}

const (
	goNorth = 1
	goSouth = 2
	goWest  = 3
	goEast  = 4

	hitWall        = 0
	moved          = 1
	atOxygenSystem = 2
)

func decideNextMove(last Direction, state State, canvas *Canvas) Direction {
	north := Direction{0, -1}
	south := Direction{0, 1}
	west := Direction{-1, 0}
	east := Direction{1, 0}

	n := canvas.Get(state.x, state.y-1)
	s := canvas.Get(state.x, state.y+1)
	w := canvas.Get(state.x-1, state.y)
	e := canvas.Get(state.x+1, state.y)

	if last == north {
		if e == '#' {
			if n != '#' {
				return north
			}
			if w != '#' {
				return west
			}
			if s != '#' {
				return south
			}
			log.Fatal("STUCK 1!")
		}
		return east
	}

	if last == west {
		if n == '#' {
			if w != '#' {
				return west
			}
			if s != '#' {
				return south
			}
			if e != '#' {
				return east
			}
			log.Fatal("STUCK 2!")
		}
		return north
	}

	if last == south {
		if w == '#' {
			if s != '#' {
				return south
			}
			if e != '#' {
				return east
			}
			if n != '#' {
				return north
			}
			log.Fatal("STUCK 3!")
		}
		return west
	}

	if last == east {
		if s == '#' {
			if e != '#' {
				return east
			}
			if n != '#' {
				return north
			}
			if w != '#' {
				return west
			}
			log.Fatal("STUCK 4!")
		}
		return south
	}

	for {
		var dir Direction
		switch rand.Int() % 4 {
		case 0:
			dir = north
		case 1:
			dir = south
		case 2:
			dir = west
		case 3:
			dir = east
		}
		if canvas.Get(state.x+dir.dx, state.y+dir.dy) != '#' {
			return dir
		}
	}
}

func doMove(dir Direction, m *IntCodeMachine, state *State, canvas *Canvas) bool {
	dir2input := map[Direction]int{
		Direction{0, -1}: goNorth,
		Direction{0, 1}:  goSouth,
		Direction{-1, 0}: goWest,
		Direction{1, 0}:  goEast,
	}

	err := m.Run([]int{dir2input[dir]})
	if err != nil {
		log.Fatal(err)
	}

	output := m.ReadOutput()
	target := Coordinate{state.x + dir.dx, state.y + dir.dy}

	switch output[0] {
	case moved, atOxygenSystem:
		state.x = target.x
		state.y = target.y

		if output[0] == atOxygenSystem {
			canvas.Set(state.x, state.y, 'X')
		} else {
			if canvas.Get(state.x, state.y) == ' ' {
				canvas.Set(state.x, state.y, '.')
			}
		}

		return true

	case hitWall:
		canvas.Set(target.x, target.y, '#')
		return false
	}

	return false
}

func spreadOxygen(canvas *Canvas) (count int) {
	for y := 0; y < canvas.height; y++ {
		for x := 0; x < canvas.width; x++ {
			if canvas.Get(x, y) == 'o' {
				canvas.Set(x, y, 'O')
			}
		}
	}

	neighbours := []Direction{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}

	for y := 1; y < canvas.height-2; y++ {
		for x := 1; x < canvas.width-2; x++ {
			if canvas.Get(x, y) == 'O' {
				for _, n := range neighbours {
					c := canvas.Get(x+n.dx, y+n.dy)
					if c == '.' || c == ',' {
						canvas.Set(x+n.dx, y+n.dy, 'o')
						count++
					}
				}
			}
		}
	}

	return count
}

func main() {
	var m IntCodeMachine
	err := m.Load("input.txt")
	if err != nil {
		log.Fatal(err)
	}

	steps := 0
	var stepsUntilFound int
	var oxygenStation Coordinate

	// Clear screen
	fmt.Println("\033c")

	canvas := NewCanvas(60, 50, true, ' ')
	canvas.Render(nil)

	start := Coordinate{canvas.width / 2, canvas.height / 2}
	state := State{start.x, start.y}

	dir := Direction{0, -1}

	allDirections := []Direction{
		Direction{0, -1},
		Direction{0, 1},
		Direction{-1, 0},
		Direction{1, 0},
	}

	for {
		for _, direction := range allDirections {
			moved := doMove(direction, &m, &state, canvas)
			if moved {
				doMove(Direction{-direction.dx, -direction.dy}, &m, &state, canvas)
			}
		}

		canvas.Render([]Sprite{{state.x, state.y, '@'}})
		fmt.Printf("Steps: %d\n", steps)

		time.Sleep(1000 * 1000 * 25)
		//fmt.Scanln()

		dir = decideNextMove(dir, state, canvas)
		doMove(dir, &m, &state, canvas)

		c := canvas.Get(state.x, state.y)

		if c == 'X' {
			steps++
			stepsUntilFound = steps
			oxygenStation = Coordinate{state.x, state.y}
		} else if c == '.' {
			canvas.Set(state.x, state.y, ',')
			steps++
		} else {
			steps--
		}

		if state.x == start.x && state.y == start.y {
			break
		}
	}

	fmt.Println("Press enter key to start filling with oxygen...")
	fmt.Scanln()

	// Part Two: fill with oxygen
	minutes := 0
	state.x = oxygenStation.x
	state.y = oxygenStation.y
	canvas.Set(state.x, state.y, 'O')
	for ; ; minutes++ {
		canvas.Render([]Sprite{})
		fmt.Printf("Minutes: %d\n", minutes)

		time.Sleep(1000 * 1000 * 100)
		// fmt.Scanln()

		n := spreadOxygen(canvas)
		if n == 0 {
			spreadOxygen(canvas)
			canvas.Render([]Sprite{})
			break
		}
	}

	fmt.Printf("Oxygen Station found at %d, %d. Shortest path: %d steps\n",
		oxygenStation.x, oxygenStation.y, stepsUntilFound)
	fmt.Printf("Time to fill with oxygen: %d minutes", minutes)
}
