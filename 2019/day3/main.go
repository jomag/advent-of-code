package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
	"strings"
)

// Segment represents one straight segment of a wire
type Segment struct {
	dir    rune
	length int
}

// Point - 2D point
type Point struct {
	x int
	y int
}

// Line - line between two 2D points
type Line struct {
	x1, y1 int
	x2, y2 int
}

// ParseSegments parse segments from comma separated values
func ParseSegments(src string) (segments []Segment, err error) {
	segStrings := strings.Split(src, ",")
	segments = make([]Segment, len(segStrings))
	for i, segString := range segStrings {
		trimmed := strings.TrimSpace(segString)
		segments[i].dir = rune(trimmed[0])
		segments[i].length, err = strconv.Atoi(trimmed[1:])

		if err != nil {
			return nil, err
		}
	}
	return segments, nil
}

func reverseLine(line Line) Line {
	return Line{line.x2, line.y2, line.x1, line.y1}
}

func findIntersection(line1, line2 Line) (Point, bool) {
	var vert, horz Line

	if line1.x1 == line1.x2 {
		if line2.x1 == line2.x2 {
			// Two vertical lines
			return Point{0, 0}, false
		}

		horz = line2
		vert = line1
	} else {
		if line2.y1 == line2.y2 {
			// Two horizontal lines
			return Point{0, 0}, false
		}

		horz = line1
		vert = line2
	}

	if horz.x1 > horz.x2 {
		horz = reverseLine(horz)
	}

	if vert.y1 > vert.y2 {
		vert = reverseLine(vert)
	}

	x, y := vert.x1, horz.y1

	if horz.x1 <= x && horz.x2 >= x && vert.y1 <= y && vert.y2 >= y {
		return Point{x, y}, true
	}

	return Point{0, 0}, false
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}

func manhattan(p Point) int {
	return abs(p.x) + abs(p.y)
}

func buildLine(p Point, seg Segment) Line {
	switch seg.dir {
	case 'U':
		return Line{p.x, p.y, p.x, p.y + seg.length}
	case 'R':
		return Line{p.x, p.y, p.x + seg.length, p.y}
	case 'D':
		return Line{p.x, p.y, p.x, p.y - seg.length}
	case 'L':
		return Line{p.x, p.y, p.x - seg.length, p.y}
	}
	return Line{0, 0, 0, 0}
}

func lineLength(line Line) int {
	return abs(line.x2-line.x1) + abs(line.y2-line.y1)
}

func findClosestIntersection(seg1 []Segment, seg2 []Segment) (int, int) {
	var l1, l2 Line
	closest := 0
	shortest := 0
	first := true
	p1 := Point{0, 0}
	len1 := 0

	for _, s1 := range seg1 {
		l1 = buildLine(p1, s1)
		p2 := Point{0, 0}
		len2 := 0

		for _, s2 := range seg2 {
			l2 = buildLine(p2, s2)
			isect, found := findIntersection(l1, l2)

			if found {
				if isect.x != 0 || isect.y != 0 {
					distance := manhattan(isect)

					if first || distance < closest {
						closest = distance
					}

					wireLen := len1 + len2 +
						lineLength(Line{l1.x1, l1.y1, isect.x, isect.y}) +
						lineLength(Line{l2.x1, l2.y1, isect.x, isect.y})

					if first || wireLen < shortest {
						shortest = wireLen
					}

					first = false
				}
			}

			len2 += lineLength(l2)
			p2 = Point{l2.x2, l2.y2}
		}

		len1 += lineLength(l1)
		p1 = Point{l1.x2, l1.y2}
	}

	return closest, shortest
}

func readInput(filename string) (path1, path2 []Segment, err error) {
	file, err := os.Open("input.txt")
	defer file.Close()

	if err != nil {
		return nil, nil, err
	}

	reader := bufio.NewReader(file)
	var lines []string
	var line string

	for {
		line, err = reader.ReadString('\n')

		if err != nil {
			break
		}

		lines = append(lines, line)
	}

	if err != io.EOF {
		return nil, nil, err
	}

	if len(lines) != 2 {
		return nil, nil, fmt.Errorf("Expected 2 lines of input, got %d", len(lines))
	}

	path1, err = ParseSegments(lines[0])

	if err != nil {
		return nil, nil, err
	}

	path2, err = ParseSegments(lines[1])

	if err != nil {
		return nil, nil, err
	}

	return path1, path2, nil
}

func main() {
	path1, path2, err := readInput("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	closest, shortest := findClosestIntersection(path1, path2)
	fmt.Printf("Closest: %d\n", closest)
	fmt.Printf("Shortest: %d\n", shortest)
}
