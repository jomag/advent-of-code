package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"sort"
	"strings"
)

// Coordinate - 2D coordinate
type Coordinate struct {
	x float64
	y float64
}

func getAsteroids(input []string) (asteroids []Coordinate) {
	for y, row := range input {
		for x := 0; x < len(row); x++ {
			if row[x] == '#' {
				asteroids = append(asteroids, Coordinate{float64(x), float64(y)})
			}
		}
	}

	return
}

func getDistance(a, b Coordinate) float64 {
	return math.Sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y))
}

func getAngle(a, b Coordinate) float64 {
	if a.x == b.x && a.y == b.y {
		log.Fatal("Can not calculate angle between two equal coordinates")
		return 0
	}

	if a.x == b.x {
		if b.y > a.y {
			return 90
		} else {
			return 270
		}
	}

	if a.y == b.y {
		if b.x > a.x {
			return 0
		} else {
			return 180
		}
	}

	rad := math.Atan((b.y - a.y) / (b.x - a.x))
	angle := rad * 180.0 / math.Pi

	if b.x > a.x {
		if b.y > a.y {
			return angle
		}

		return angle + 360
	}

	return 180 + angle
}

func findBestBase(input []string) Coordinate {
	asteroids := getAsteroids(input)

	bestIndex := -1
	bestCount := -1

	for a, base := range asteroids {
		count := 0
		for b, target := range asteroids {
			if a != b {
				targetAngle := getAngle(base, target)
				obscured := false
				for c, obstacle := range asteroids {
					if a != c && b != c {
						obstacleAngle := getAngle(base, obstacle)
						if math.Abs(targetAngle-obstacleAngle) < 0.001 {
							if getDistance(base, obstacle) < getDistance(base, target) {
								obscured = true
							}
						}
					}
				}
				if !obscured {
					count = count + 1
				}
			}
		}
		if count > bestCount {
			bestCount = count
			bestIndex = a
		}
	}

	fmt.Printf("Best count: %d\n", bestCount)
	fmt.Printf("Best index: %d\n", bestIndex)
	fmt.Printf("Best base:")
	fmt.Println(asteroids[bestIndex])
	return asteroids[bestIndex]
}

func readInput(filename string) (source []string, err error) {
	raw, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	text := string(raw)
	return strings.Split(text, "\n"), nil
}

// Asteroid - coordinate and angle + distance relative base asteroid
type Asteroid struct {
	x        float64
	y        float64
	angle    float64
	distance float64
}

func angleDiff(a, b float64) float64 {
	diff := b - a
	diff = math.Mod(diff+180.0, 360.0) - 180.0
	if diff < 0 {
		return diff + 360.0
	}
	return diff
}

func normalizeAngle(a float64) float64 {
	if a < 0 {
		return a + 360
	}
	return a
}

func partTwo(base Coordinate, asteroids []Coordinate) []Asteroid {
	var list []Asteroid

	for _, asteroid := range asteroids {
		if base.x != asteroid.x || base.y != asteroid.y {
			angle := normalizeAngle(getAngle(base, asteroid) - 270)
			distance := getDistance(base, asteroid)
			list = append(list, Asteroid{asteroid.x, asteroid.y, angle, distance})
		}
	}

	sort.Slice(list, func(i, j int) bool {
		return list[i].distance < list[j].distance
	})

	sort.SliceStable(list, func(i, j int) bool {
		return list[i].angle < list[j].angle
	})

	// Find first
	var kills []Asteroid

	dir := list[0].angle
	kills = append(kills, list[0])
	list = list[1:]
	i := 0

	for len(list) > 0 {
		var j int
		for j = 0; j < len(list) && list[(i+j)%len(list)].angle-dir < 0.0001; j++ {
		}

		i = (i + j) % len(list)
		dir = list[i].angle
		kills = append(kills, list[i])
		list = append(list[:i], list[i+1:]...)
	}

	return kills
}

func main() {
	examples := [][]string{
		{
			".#..#",
			".....",
			"#####",
			"....#",
			"...##",
		},
		{
			"......#.#.",
			"#..#.#....",
			"..#######.",
			".#.#.###..",
			".#..#.....",
			"..#....#.#",
			"#..#....#.",
			".##.#..###",
			"##...#..#.",
			".#....####",
		},
		{
			"#.#...#.#.",
			".###....#.",
			".#....#...",
			"##.#.#.#.#",
			"....#.#.#.",
			".##..###.#",
			"..#...##..",
			"..##....##",
			"......#...",
			".####.###.",
		},
		{
			".#..#..###",
			"####.###.#",
			"....###.#.",
			"..###.##.#",
			"##.##.#.#.",
			"....###..#",
			"..#.#..#.#",
			"#..#.#.###",
			".##...##.#",
			".....#.#..",
		},
		{
			".#..##.###...#######",
			"##.############..##.",
			".#.######.########.#",
			".###.#######.####.#.",
			"#####.##.#.##.###.##",
			"..#####..#.#########",
			"####################",
			"#.####....###.#.#.##",
			"##.#################",
			"#####.##.###..####..",
			"..######..##.#######",
			"####.##.####...##..#",
			".#####..#.######.###",
			"##...#.##########...",
			"#.##########.#######",
			".####.#.###.###.#.##",
			"....##.##.###..#####",
			".#.#.###########.###",
			"#.#.#.#####.####.###",
			"###.##.####.##.#..##",
		},
	}

	fmt.Println("Part One:")
	for n, example := range examples {
		fmt.Printf("\nExample %d:\n", n)
		findBestBase(example)
	}

	partOneInput, err := readInput("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("\nPart One result:")
	base := findBestBase(partOneInput)

	fmt.Println("\nPart Two:")
	kills := partTwo(Coordinate{11, 13}, getAsteroids(examples[4]))
	fmt.Println("\nExample:")
	for _, i := range []int{1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299} {
		fmt.Printf("Asteroid %d: %g,%g\n", i, kills[i-1].x, kills[i-1].y)
	}

	fmt.Println("\nPart Two result:")
	kills = partTwo(base, getAsteroids(partOneInput))
	fmt.Printf("200th: %g,%g (%g)", kills[199].x, kills[199].y, kills[199].x*100+kills[199].y)
}
