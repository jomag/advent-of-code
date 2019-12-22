package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"sort"
	"strings"
)

func printDistanceMap(distanceMap *DistanceMap, canvas *Canvas) {
	output := ""
	for y := 0; y < canvas.height; y++ {
		for x := 0; x < canvas.width; x++ {
			n := distanceMap.get(x, y)
			if n < 0 {
				output += " " + strings.Repeat(string(canvas.Get(x, y)), 2)
			} else {
				output += fmt.Sprintf(" %02d", n)
			}
		}
		output += "\n"
	}

	fmt.Println(output)
}

// DistanceMap should have comment
type DistanceMap struct {
	width, height int
	buf           []int
}

func newDistanceMap(canvas *Canvas) (distanceMap *DistanceMap) {
	distanceMap = new(DistanceMap)
	distanceMap.width = canvas.width
	distanceMap.height = canvas.height
	distanceMap.buf = make([]int, canvas.width*canvas.height)
	for i := range distanceMap.buf {
		distanceMap.buf[i] = -1
	}
	return
}

func (distanceMap *DistanceMap) get(x, y int) int {
	return distanceMap.buf[y*distanceMap.width+x]
}

func (distanceMap *DistanceMap) set(x, y, value int) {
	distanceMap.buf[y*distanceMap.width+x] = value
}

// Option should have comment
type Option struct {
	id       byte
	pos      Coordinate
	distance int
}

func (option Option) String() string {
	return fmt.Sprintf("%c@%d,%d (%d)", option.id, option.pos.x, option.pos.y, option.distance)
}

func getOptions(player Coordinate, canvas *Canvas, remaining []byte) []Option {
	dmap := newDistanceMap(canvas)
	dmap.set(player.x, player.y, 0)
	var options []Option

	for {
		complete := true
		for y := 1; y < canvas.height-1; y++ {
			for x := 1; x < canvas.width-1; x++ {
				if canvas.Get(x, y) != '#' && dmap.get(x, y) == -1 {
					neighbours := []int{
						dmap.get(x, y-1),
						dmap.get(x, y+1),
						dmap.get(x-1, y),
						dmap.get(x+1, y),
					}

					distance := -1
					for _, n := range neighbours {
						if n >= 0 && (distance < 0 || n < distance) {
							distance = n + 1
						}
					}

					if distance >= 0 {
						o := canvas.Get(x, y)
						if o == '.' {
							dmap.set(x, y, distance)
						}
						if isKey(o) {
							if contains(remaining, o) {
								options = append(options, Option{o, Coordinate{x, y}, distance})
								dmap.set(x, y, -2)
							} else {
								dmap.set(x, y, distance)
							}
						}
						if isDoor(o) {
							if contains(remaining, o) && !contains(remaining, o+32) {
								options = append(options, Option{o, Coordinate{x, y}, distance})
								dmap.set(x, y, -2)
							} else {
								dmap.set(x, y, distance)
							}
						}
						complete = false
					}
				}
			}
		}
		if complete {
			break
		}
	}

	// printDistanceMap(dmap, canvas)
	return options
}

func isKey(id byte) bool {
	return id >= 'a' && id <= 'z'
}

func isDoor(id byte) bool {
	return id >= 'A' && id <= 'Z'
}

func contains(haystack []byte, needle byte) bool {
	for _, v := range haystack {
		if needle == v {
			return true
		}
	}
	return false
}

func remove(list []byte, value byte) (list2 []byte) {
	for _, c := range list {
		if c != value {
			list2 = append(list2, c)
		}
	}
	return
}

func solve2(input string) {
	canvas := NewCanvasFromString(input)
	canvas.Render([]Sprite{}, false)

	//var distances map[byte]map[byte]int

	// Step 1: find all doors and keys
	var keys []byte
	var doors []byte
	for y := 0; y < canvas.height; y++ {
		for x := 0; x < canvas.width; x++ {
			c := canvas.Get(x, y)
			if isDoor(c) {
				doors = append(doors, c)
			}
			if isKey(c) {
				keys = append(keys, c)
			}
		}
	}

	fmt.Printf("Doors: %s\n", doors)
	fmt.Printf("Keys: %s\n", keys)

	// Recursive solver
	var recurse func(from Coordinate, remaining []byte, canvas *Canvas, indent string) (shortest int)
	precomputed := make(map[string]int)
	recurse = func(from Coordinate, remaining []byte, canvas *Canvas, indent string) (shortest int) {
		sort.Slice(remaining, func(i, j int) bool {
			return remaining[i] < remaining[j]
		})
		uff := fmt.Sprintf("%d,%d->%s", from.x, from.y, remaining)

		best, found := precomputed[uff]
		if found {
			return best
		}

		options := getOptions(from, canvas, remaining)
		fmt.Printf("%s%v %s\n", indent, options, remaining)

		best = 0
		for _, opt := range options {
			shortest2 := recurse(opt.pos, remove(remaining, opt.id), canvas, indent+"  ")

			if best == 0 || opt.distance+shortest2 < best {
				best = opt.distance + shortest2
			}
		}

		precomputed[uff] = best
		return best
	}

	// Find start position
	player, err := canvas.Find('@')
	if err != nil {
		log.Fatal("Player not found!")
	}
	canvas.Set(player.x, player.y, '.')
	all := append(keys, doors...)
	options := getOptions(player, canvas, all)
	// fmt.Println("%v %s\n", options, remove(all, opt.id))
	best := -1
	for _, opt := range options {
		result := recurse(opt.pos, remove(all, opt.id), canvas, "  ")
		if best < 0 || opt.distance+result < best {
			best = opt.distance + result
		}
	}
	fmt.Printf("Result: %d\n", best)
}

func solve(input string) {
	var recurse func(target Option, distance2 int, keys []byte, canvas *Canvas, indent string) (path string, distance int)

	shortestTotal := -1

	recurse = func(target Option, distance2 int, keys []byte, canvas *Canvas, indent string) (path string, distance int) {
		if distance2 >= shortestTotal && shortestTotal >= 0 {
			return "", -1
		}

		fmt.Println(indent)
		// fmt.Printf("%srecurse(target=%v, keys=%v)\n", indent, target, keys)
		canvas.Set(target.pos.x, target.pos.y, '.')

		newKeys := append([]byte{}, keys...)
		if isKey(target.id) {
			newKeys = append(newKeys, target.id)
		}

		options := getOptions(target.pos, canvas, newKeys)
		//fmt.Printf("Options: %d\n", len(options))

		if len(options) == 0 {
			if shortestTotal < 0 || shortestTotal > distance2+target.distance {
				shortestTotal = distance2 + target.distance
				fmt.Printf("New shortest found: %d\n", shortestTotal)
			}
			return string(target.id), target.distance
		}

		shortest := -1
		shortestPath := ""
		for _, opt := range options {
			if isKey(opt.id) || contains(newKeys, opt.id+32) {
				path, dist := recurse(opt, distance2+target.distance, newKeys, canvas.Clone(), fmt.Sprintf("%s->%s[%d]", indent, string(target.id), len(options)))
				if (dist > 0 && dist < shortest) || shortest < 0 {
					shortest = dist
					shortestPath = path
				}
			}
		}

		if shortest < 0 {
			return string(target.id), target.distance
		}

		return fmt.Sprintf("%s, %s", string(target.id), shortestPath), target.distance + shortest
	}

	canvas := NewCanvasFromString(input)
	canvas.Render([]Sprite{}, false)
	fmt.Printf("Width %d, Height %d\n", canvas.width, canvas.height)

	player, err := canvas.Find('@')
	canvas.Set(player.x, player.y, '.')
	if err != nil {
		log.Fatal("Player not found!")
	}

	options := getOptions(player, canvas, []byte{})
	fmt.Println("First options:")
	fmt.Println(options)
	shortest := -2
	shortestPath := ""
	for _, opt := range options {
		fmt.Printf("Trying base option %v\n", opt)
		if isKey(opt.id) {
			path, distance := recurse(opt, 0, []byte{}, canvas.Clone(), "@")
			if distance > 0 && (distance < shortest || shortest < 0) {
				shortest = distance
				shortestPath = path
			}
		}
	}

	fmt.Printf("Shortest: %d => %s \n", shortest, shortestPath)
}

func main() {
	raw, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	puzzleInput := strings.Split(string(raw), "\n")

	inputs := [][]string{
		// {
		// 	"#########",
		// 	"#b.A.@.a#",
		// 	"#########",
		// },
		// {
		// 	"########################",
		// 	"#f.D.E.e.C.b.A.@.a.B.c.#",
		// 	"######################.#",
		// 	"#d.....................#",
		// 	"########################",
		// },
		// {
		// 	"########################",
		// 	"#...............b.C.D.f#",
		// 	"#.######################",
		// 	"#.....@.a.B.c.d.A.e.F.g#",
		// 	"########################",
		// },
		// {
		// 	"#################",
		// 	"#i.G..c...e..H.p#",
		// 	"########.########",
		// 	"#j.A..b...f..D.o#",
		// 	"########@########",
		// 	"#k.E..a...g..B.n#",
		// 	"########.########",
		// 	"#l.F..d...h..C.m#",
		// 	"#################",
		// },
		// {
		// 	"########################",
		// 	"#@..............ac.GI.b#",
		// 	"###d#e#f################",
		// 	"###A#B#C################",
		// 	"###g#h#i################",
		// 	"########################",
		// },
		puzzleInput,
	}

	for _, input := range inputs {
		solve2(strings.Join(input, "\n"))
	}

	fmt.Println("Done!")
}
