package main

import (
	"fmt"
	"io/ioutil"
	"log"
)

// Portal should have comment
type Portal struct {
	inner Coordinate
	outer Coordinate
}

// Maze should have comment
type Maze struct {
	start   Coordinate
	end     Coordinate
	portals map[string]Portal
}

func (maze *Maze) addPortal(name string, pos Coordinate, outer bool) {
	if name == "AA" {
		maze.start = pos
	} else if name == "ZZ" {
		maze.end = pos
	} else {
		p, found := maze.portals[name]
		if found {
			if outer {
				maze.portals[name] = Portal{p.inner, pos}
			} else {
				maze.portals[name] = Portal{pos, p.outer}
			}
		} else {
			if outer {
				maze.portals[name] = Portal{Coordinate{-1, -1}, pos}
			} else {
				maze.portals[name] = Portal{pos, Coordinate{-1, -1}}
			}
		}
	}
}

func createCanvas(filename string) (*Canvas, error) {
	raw, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	content := string(raw)
	if content[len(content)-1] == '\n' {
		content = content[:len(content)-1]
	}

	canvas := NewCanvasFromString(content)
	return canvas, nil
}

func findCenterArea(canvas *Canvas) (x, y, w, h int) {
	for y := 2; y < canvas.height-2; y++ {
		for x := 2; x < canvas.width-2; x++ {
			c := canvas.Get(x, y)
			if c != '#' && c != '.' {
				for w = 0; x+w < canvas.width-2; w++ {
					c = canvas.Get(x+w, y)
					if c == '#' || c == '.' {
						for h = 0; y+h < canvas.height-2; h++ {
							c = canvas.Get(x, y+h)
							if c == '#' || c == '.' {
								return x, y, w, h
							}
						}
					}
				}
			}
		}
	}
	return 0, 0, 0, 0
}

func loadMaze(filename string) (*Canvas, *Maze, error) {
	canvas, err := createCanvas(filename)
	if err != nil {
		return nil, nil, err
	}

	maze := new(Maze)
	maze.portals = make(map[string]Portal)

	// Scan entrances at top and bottom
	for x := 2; x < canvas.width-2; x++ {
		a, b := canvas.Get(x, 0), canvas.Get(x, 1)
		if a != ' ' && b != ' ' {
			maze.addPortal(string(a)+string(b), Coordinate{x, 2}, true)
		}

		a, b = canvas.Get(x, canvas.height-2), canvas.Get(x, canvas.height-1)
		if a != ' ' && b != ' ' {
			maze.addPortal(string(a)+string(b), Coordinate{x, canvas.height - 3}, true)
		}
	}

	// Scan entrances at left and right
	for y := 2; y < canvas.height-2; y++ {
		a, b := canvas.Get(0, y), canvas.Get(1, y)
		if a != ' ' && b != ' ' {
			maze.addPortal(string(a)+string(b), Coordinate{2, y}, true)
		}

		a, b = canvas.Get(canvas.width-2, y), canvas.Get(canvas.width-1, y)
		if a != ' ' && b != ' ' {
			maze.addPortal(string(a)+string(b), Coordinate{canvas.width - 3, y}, true)
		}
	}

	// Scan inner entrances: left, right, top and bottom
	cx, cy, cw, ch := findCenterArea(canvas)

	for y := cy; y < cy+ch; y++ {
		a, b := canvas.Get(cx, y), canvas.Get(cx+1, y)
		if a != ' ' && b != ' ' {
			maze.addPortal(string(a)+string(b), Coordinate{cx - 1, y}, false)
		}

		a, b = canvas.Get(cx+cw-2, y), canvas.Get(cx+cw-1, y)
		if a != ' ' && b != ' ' {
			maze.addPortal(string(a)+string(b), Coordinate{cx + cw, y}, false)
		}
	}

	for x := cx; x < cx+cw; x++ {
		a, b := canvas.Get(x, cy), canvas.Get(x, cy+1)
		if a != ' ' && b != ' ' {
			maze.addPortal(string(a)+string(b), Coordinate{x, cy - 1}, false)
		}

		a, b = canvas.Get(x, cy+ch-2), canvas.Get(x, cy+ch-1)
		if a != ' ' && b != ' ' {
			maze.addPortal(string(a)+string(b), Coordinate{x, cy + ch}, false)
		}
	}

	return canvas, maze, nil
}

// Node should have comment
type Node struct {
	x        int
	y        int
	distance int
	level    int
	path     string
}

func partOne(filename string) (int, error) {
	canvas, maze, err := loadMaze(filename)
	if err != nil {
		return 0, err
	}

	// canvas.Render([]Sprite{}, false)
	queue := []Node{Node{maze.start.x, maze.start.y, 0, 0, fmt.Sprintf("(%d,%d)", maze.start.x, maze.start.y)}}
	visited := make([]bool, canvas.width*canvas.height)

	teleport := func(pos Coordinate) Coordinate {
		for _, portal := range maze.portals {
			if portal.inner.x == pos.x && portal.inner.y == pos.y {
				return portal.outer
			}
			if portal.outer.x == pos.x && portal.outer.y == pos.y {
				return portal.inner
			}
		}

		return pos
	}

	for len(queue) > 0 {
		node := queue[0]

		idx := canvas.width*node.y + node.x
		if !visited[idx] {
			visited[idx] = true

			if node.x == maze.end.x && node.y == maze.end.y {
				fmt.Printf("Found exit in %d steps\n", node.distance)
				// fmt.Printf("Path: %s\n", node.path)
				return node.distance, nil
			}

			neighbours := [4]Coordinate{
				{node.x, node.y - 1},
				{node.x, node.y + 1},
				{node.x - 1, node.y},
				{node.x + 1, node.y},
			}

			for _, npos := range neighbours {
				distance := node.distance + 1
				pos := teleport(npos)
				if pos != npos {
					distance++
				}
				c := canvas.Get(pos.x, pos.y)
				if c == '.' {
					queue = append(queue, Node{
						pos.x,
						pos.y,
						distance,
						0,
						fmt.Sprintf("%s->(%d,%d)", node.path, pos.x, pos.y),
					})
				}
			}
		}

		queue = queue[1:]
	}

	fmt.Println("No solution found")
	return 0, nil
}

func partTwo(filename string) (int, error) {
	canvas, maze, err := loadMaze(filename)

	if err != nil {
		return 0, err
	}

	// canvas.Render([]Sprite{}, false)
	queue := []Node{Node{maze.start.x, maze.start.y, 0, 0, fmt.Sprintf("(%d,%d)", maze.start.x, maze.start.y)}}
	var visited [][]bool

	teleport := func(pos Coordinate, level int) (Coordinate, int) {
		for _, portal := range maze.portals {
			if portal.inner.x == pos.x && portal.inner.y == pos.y {
				return portal.outer, level + 1
			}
			if level > 0 {
				if portal.outer.x == pos.x && portal.outer.y == pos.y {
					return portal.inner, level - 1
				}
			}
		}

		return pos, level
	}

	for len(queue) > 0 {
		node := queue[0]

		for len(visited) <= node.level {
			visited = append(visited, make([]bool, canvas.width*canvas.height))
		}

		idx := canvas.width*node.y + node.x
		if !visited[node.level][idx] {
			visited[node.level][idx] = true

			if node.level == 0 && node.x == maze.end.x && node.y == maze.end.y {
				fmt.Printf("Found exit in %d steps\n", node.distance)
				// fmt.Printf("Path: %s\n", node.path)
				return node.distance, nil
			}

			neighbours := [4]Coordinate{
				{node.x, node.y - 1},
				{node.x, node.y + 1},
				{node.x - 1, node.y},
				{node.x + 1, node.y},
			}

			for _, npos := range neighbours {
				distance := node.distance + 1
				level := node.level
				pos, level := teleport(npos, level)
				if pos != npos {
					distance++
				}
				c := canvas.Get(pos.x, pos.y)
				if c == '.' {
					isVisited := len(visited) > level && visited[level][pos.y*canvas.width+pos.x]
					if !isVisited {
						queue = append(queue, Node{
							pos.x,
							pos.y,
							distance,
							level,
							fmt.Sprintf("%s->(%d,%d)", node.path, pos.x, pos.y),
						})
					}
				}
			}
		}

		queue = queue[1:]
	}

	fmt.Println("No solution found")
	return 0, nil
}

func main() {
	fmt.Println("Part One\n========")
	for _, filename := range []string{"example1.txt", "example2.txt", "input.txt"} {
		fmt.Printf("\n%s:\n", filename)
		_, err := partOne(filename)
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Println("\n\nPart Two\n========")
	for _, filename := range []string{"example1.txt", "example3.txt", "input.txt"} {
		fmt.Printf("\n%s:\n", filename)
		_, err := partTwo(filename)
		if err != nil {
			log.Fatal(err)
		}
	}
}
