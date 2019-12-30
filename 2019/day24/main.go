package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"sort"
	"strings"
)

// Board should have comment
type Board struct {
	width  int
	height int
	board  []bool
}

// MultiBoard should have comment
type MultiBoard struct {
	boards map[int]*Board
}

func (multi *MultiBoard) getAdjacentCount(level, x, y int) (count int) {
	board := multi.boards[level]

	above, hasAbove := multi.boards[level+1]
	below, hasBelow := multi.boards[level-1]

	// Left
	if x == 0 {
		if hasAbove && above.get(1, 2) {
			count++
		}
	} else if x == 3 && y == 2 {
		if hasBelow {
			for ry := 0; ry < 5; ry++ {
				if below.get(4, ry) {
					count++
				}
			}
		}
	} else {
		if board != nil && board.get(x-1, y) {
			count++
		}
	}

	// Right
	if x == 4 {
		if hasAbove && above.get(3, 2) {
			count++
		}
	} else if x == 1 && y == 2 {
		if hasBelow {
			for ry := 0; ry < 5; ry++ {
				if below.get(0, ry) {
					count++
				}
			}
		}
	} else {
		if board != nil && board.get(x+1, y) {
			count++
		}
	}

	// Top
	if y == 0 {
		if hasAbove && above.get(2, 1) {
			count++
		}
	} else if y == 3 && x == 2 {
		if hasBelow {
			for rx := 0; rx < 5; rx++ {
				if below.get(rx, 4) {
					count++
				}
			}
		}
	} else {
		if board != nil && board.get(x, y-1) {
			count++
		}
	}

	// Bottom
	if y == 4 {
		if hasAbove && above.get(2, 3) {
			count++
		}
	} else if y == 1 && x == 2 {
		if hasBelow {
			for rx := 0; rx < 5; rx++ {
				if below.get(rx, 0) {
					count++
				}
			}
		}
	} else {
		if board != nil && board.get(x, y+1) {
			count++
		}
	}

	return
}

// ToString should have comment
func (board *Board) ToString() string {
	s := ""
	for i := 0; i < board.width*board.height; i++ {
		if i > 0 && i%board.width == 0 {
			s = s + "\n"
		}
		if board.board[i] {
			s = s + "#"
		} else {
			s = s + "."
		}
	}
	return s
}

func (board *Board) get(x, y int) bool {
	if x < 0 || x >= board.width {
		return false
	}
	if y < 0 || y >= board.height {
		return false
	}
	return board.board[y*board.width+x]
}

func (multi *MultiBoard) get(level, x, y int) bool {
	if board, ok := multi.boards[level]; ok {
		return board.get(x, y)
	}
	return false
}

func (board *Board) getAdjacentCount(x, y int) (count int) {
	if board.get(x-1, y) {
		count++
	}
	if board.get(x+1, y) {
		count++
	}
	if board.get(x, y-1) {
		count++
	}
	if board.get(x, y+1) {
		count++
	}
	return
}

func (board *Board) getBiodiversityRating() (rating int) {
	for i, cell := range board.board {
		if cell {
			rating = rating | (1 << i)
		}
	}
	return
}

func (board *Board) getCount() (count int) {
	for _, cell := range board.board {
		if cell {
			count++
		}
	}
	return
}

func (multi *MultiBoard) getCount() (count int) {
	for _, board := range multi.boards {
		count += board.getCount()
	}
	return
}

func (board *Board) step() {
	newBoard := make([]bool, len(board.board))
	for y := 0; y < board.height; y++ {
		for x := 0; x < board.width; x++ {
			c := board.getAdjacentCount(x, y)
			if board.get(x, y) {
				newBoard[board.width*y+x] = c == 1
			} else {
				newBoard[board.width*y+x] = c == 1 || c == 2
			}
		}
	}
	board.board = newBoard
}

func (board *Board) clone() (clone *Board) {
	clone = new(Board)
	clone.width = board.width
	clone.height = board.height
	clone.board = make([]bool, len(board.board))
	for i, cell := range board.board {
		clone.board[i] = cell
	}
	return
}

func (multi *MultiBoard) step() {
	newBoardMap := make(map[int]*Board)
	highest := 0
	lowest := 0

	for level := range multi.boards {
		if level < lowest {
			lowest = level
		}
		if level > highest {
			highest = level
		}
	}

	for level := lowest - 1; level <= highest+1; level++ {
		newBoardMap[level] = &Board{5, 5, make([]bool, 5*5)}
	}

	for level, board := range newBoardMap {
		for y := 0; y < 5; y++ {
			for x := 0; x < 5; x++ {
				if y != 2 || x != 2 {
					c := multi.getAdjacentCount(level, x, y)
					if multi.get(level, x, y) {
						board.board[board.width*y+x] = c == 1
					} else {
						board.board[board.width*y+x] = c == 1 || c == 2
					}
				}
			}
		}
	}

	multi.boards = newBoardMap
}

// ToString should have comment
func (multi *MultiBoard) ToString() (str string) {
	levels := make([]int, 0)
	for level := range multi.boards {
		levels = append(levels, level)
	}
	sort.Ints(levels)

	for _, level := range levels {
		str = str + fmt.Sprintf("Level %d\n", level)
		str = str + multi.boards[level].ToString() + "\n\n"
	}
	return
}

func loadBoard(filename string) (board *Board, err error) {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	lines := strings.Split(string(content), "\n")
	board = new(Board)
	board.width = len(lines[0])
	board.height = 0
	board.board = make([]bool, board.width*board.height)
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if len(trimmed) > 0 {
			board.height++
			row := make([]bool, board.width)
			for j, char := range strings.TrimSpace(line) {
				row[j] = char == '#'
			}
			board.board = append(board.board, row...)
		}
	}
	return board, nil
}

func main() {
	board, err := loadBoard("input.txt")
	ratings := make(map[int]bool)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Print("Part One\n========\n\n")
	for {
		// fmt.Println(board.ToString())
		// fmt.Println(board.getBiodiversityRating())
		// fmt.Scanln()

		board.step()
		rating := board.getBiodiversityRating()
		if _, ok := ratings[rating]; ok {
			fmt.Printf("First repeated biodiversity rating: %d\n", rating)
			break
		}
		ratings[rating] = true
	}

	fmt.Print("\nPart Two\n========\n\n")
	board, err = loadBoard("input.txt")
	multiBoard := MultiBoard{map[int]*Board{0: board}}
	minutes := 200

	for minute := 0; minute < minutes; minute++ {
		// fmt.Printf("Minute %d:\n--------------------\n\n", minute)
		// fmt.Print(multiBoard.ToString())
		// fmt.Scanln()

		multiBoard.step()
	}

	fmt.Printf("Bugs after %d minutes: %d\n", minutes, multiBoard.getCount())
}
