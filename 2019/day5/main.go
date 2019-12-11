package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

const (
	// OpAdd - Add operator
	OpAdd = 1
	// OpMul - Multiply operator
	OpMul = 2
	// OpInput - Read input operator
	OpInput = 3
	// OpOutput - Print/output operator
	OpOutput = 4
	// OpJumpIfTrue - Jump if true
	OpJumpIfTrue = 5
	// OpJumpIfFalse - Jump if false
	OpJumpIfFalse = 6
	// OpLess - Set true if op 1 < op 2
	OpLess = 7
	// OpEqual - Set true if op 1 == op2
	OpEqual = 8
	// OpHalt - Halt operator
	OpHalt = 99
)

func readParameter(param int, buf []int, offs int) int {
	var mode int
	switch param {
	case 0:
		mode = buf[offs] / 100 % 10
	case 1:
		mode = buf[offs] / 1000 % 10
	case 2:
		mode = buf[offs] / 10000 % 10
	case 3:
		mode = buf[offs] / 100000 % 10
	case 4:
		mode = buf[offs] / 1000000 % 10
	}

	addr := buf[offs+param+1]

	// fmt.Printf("OP: %d, Mode: %d\n", buf[offs], mode)

	if mode == 0 {
		// Position mode
		return buf[addr]
	}

	if mode == 1 {
		// Immediate mode
		return addr
	}

	return 0
}

func runIntCode(program []int, input int) (output []int, err error) {
	buf := make([]int, len(program))
	copy(buf[:], program)
	pc := 0

	for {
		if buf[pc] == OpHalt {
			break
		}

		// fmt.Printf("Next: %d (@%d)\n", buf[pc], pc)

		switch buf[pc] % 100 {
		case OpAdd:
			op1 := readParameter(0, buf, pc)
			op2 := readParameter(1, buf, pc)
			dst := buf[pc+3]
			buf[dst] = op1 + op2
			pc += 4
		case OpMul:
			op1 := readParameter(0, buf, pc)
			op2 := readParameter(1, buf, pc)
			dst := buf[pc+3]
			buf[dst] = op1 * op2
			pc += 4
		case OpInput:
			dst := buf[pc+1]
			buf[dst] = input
			pc += 2
		case OpOutput:
			op1 := readParameter(0, buf, pc)
			fmt.Println(op1)
			pc += 2
		case OpJumpIfTrue:
			op1 := readParameter(0, buf, pc)
			op2 := readParameter(1, buf, pc)
			if op1 != 0 {
				pc = op2
			} else {
				pc += 3
			}
		case OpJumpIfFalse:
			op1 := readParameter(0, buf, pc)
			op2 := readParameter(1, buf, pc)
			if op1 == 0 {
				pc = op2
			} else {
				pc += 3
			}
		case OpLess:
			op1 := readParameter(0, buf, pc)
			op2 := readParameter(1, buf, pc)
			dst := buf[pc+3]
			if op1 < op2 {
				buf[dst] = 1
			} else {
				buf[dst] = 0
			}
			pc += 4
		case OpEqual:
			op1 := readParameter(0, buf, pc)
			op2 := readParameter(1, buf, pc)
			dst := buf[pc+3]
			if op1 == op2 {
				buf[dst] = 1
			} else {
				buf[dst] = 0
			}
			pc += 4
		default:
			return nil, fmt.Errorf("Invalid operator '%d' at index %d", buf[pc], pc)
		}

		if pc >= len(buf) {
			return nil, fmt.Errorf("Reached end of code")
		}
	}

	return buf, nil
}

func readInput(filename string) (data []int, err error) {
	raw, err := ioutil.ReadFile(filename)

	if err != nil {
		return nil, err
	}

	text := string(raw)
	nums := strings.Split(text, ",")
	code := make([]int, len(nums))
	for i, num := range nums {
		code[i], err = strconv.Atoi(strings.TrimSpace(num))
		if err != nil {
			return nil, err
		}
	}

	return code, nil
}

func main() {
	prg, err := readInput("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("\nPart one:")
	_, err = runIntCode(prg, 1)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("\nPart two:")
	_, err = runIntCode(prg, 5)

	if err != nil {
		log.Fatal(err)
	}
}
