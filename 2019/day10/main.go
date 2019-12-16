package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
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

func findBestBase(input []string) {
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
}

func readInput(filename string) (source []string, err error) {
	raw, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	text := string(raw)
	return strings.Split(text, "\n"), nil
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

	for n, example := range examples {
		fmt.Printf("\nExample %d:\n", n)
		findBestBase(example)
	}

	partOneInput, err := readInput("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("\nPart One:")
	findBestBase(partOneInput)
}
