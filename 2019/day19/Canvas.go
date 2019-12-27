package main

import (
	"errors"
	"fmt"
	"strings"
)

// Coordinate should have comment.
type Coordinate struct {
	x, y int
}

// Sprite should have comment.
type Sprite struct {
	x, y int
	char byte
}

// Canvas - display buffer
type Canvas struct {
	width   int
	height  int
	buffer  []byte
	border  bool
	columns int
	rows    int
	offset  Coordinate
}

// NewCanvasFromString should have comment
func NewCanvasFromString(str string) (canvas *Canvas) {
	width := strings.Index(str, "\n")
	height := len(str) / width

	canvas = NewCanvas(width, height, true, ' ')
	canvas.Draw(str)
	return canvas
}

// NewCanvas - Allocate, initiate and return a new Canvas
func NewCanvas(width, height int, border bool, fill byte) (canvas *Canvas) {
	canvas = new(Canvas)
	canvas.width = width
	canvas.height = height
	canvas.columns = width + 1
	canvas.rows = height
	canvas.offset = Coordinate{0, 0}

	if border {
		canvas.columns += 2
		canvas.rows += 2
		canvas.offset = Coordinate{1, 1}
	}

	canvas.buffer = make([]byte, (canvas.columns)*canvas.rows)

	for i := range canvas.buffer {
		if (i+1)%(canvas.columns) == 0 {
			canvas.buffer[i] = '\n'
		} else {
			canvas.buffer[i] = fill
		}
	}

	if border {
		for i := 1; i < canvas.columns-2; i++ {
			canvas.buffer[i] = '-'
			canvas.buffer[canvas.columns*(canvas.rows-1)+i] = '-'
		}

		for i := 1; i < canvas.rows-1; i++ {
			canvas.buffer[canvas.columns*i] = '|'
			canvas.buffer[canvas.columns*(i+1)-2] = '|'
		}

		canvas.buffer[0] = '+'
		canvas.buffer[canvas.columns-2] = '+'
		canvas.buffer[canvas.columns*(canvas.rows-1)] = '+'
		canvas.buffer[canvas.columns*canvas.rows-2] = '+'
	}

	return canvas
}

// Clone should have comment
func (c *Canvas) Clone() (clone *Canvas) {
	clone = new(Canvas)
	*clone = *c
	clone.buffer = append([]byte{}, c.buffer...)
	return
}

// Draw should have comment.
func (c *Canvas) Draw(img string) {
	lines := strings.Split(img, "\n")

	for y, line := range lines {
		for x := range line {
			c.Set(x, y, line[x])
		}
	}
}

// Get - get character at x,y
func (c *Canvas) Get(x, y int) byte {
	if x < 0 || x >= c.width || y < 0 || y >= c.height {
		return 0
	}

	idx := (y+c.offset.y)*c.columns + x + c.offset.x
	return c.buffer[idx]
}

// Set - set character at x,y
func (c *Canvas) Set(x, y int, char byte) {
	idx := (y+c.offset.y)*c.columns + x + c.offset.x
	c.buffer[idx] = char
}

// Find - find position of character
func (c *Canvas) Find(char byte) (Coordinate, error) {
	for y := 0; y < c.height; y++ {
		for x := 0; x < c.width; x++ {
			if c.Get(x, y) == char {
				return Coordinate{x, y}, nil
			}
		}
	}

	return Coordinate{0, 0}, errors.New("Not found")
}

// Render - render display buffer
func (c *Canvas) Render(sprites []Sprite, clear bool) {
	prev := make([]byte, len(sprites))

	for i, sprite := range sprites {
		prev[i] = c.Get(sprite.x, sprite.y)
		c.Set(sprite.x, sprite.y, sprite.char)
	}

	if clear {
		fmt.Println("\033[0;0H")
	}

	fmt.Print(string(c.buffer))

	for i, sprite := range sprites {
		c.Set(sprite.x, sprite.y, prev[i])
	}
}
