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
	// OpHalt - Halt operator
	OpHalt = 99
)

func runIntCode(input []int) (output []int, err error) {
	buf := make([]int, len(input))
	copy(buf[:], input)
	pc := 0

	for {
		if buf[pc] == OpHalt {
			break
		}

		switch buf[pc] {
		case OpAdd:
			op1 := buf[pc+1]
			op2 := buf[pc+2]
			dst := buf[pc+3]
			buf[dst] = buf[op1] + buf[op2]
			pc += 4
		case OpMul:
			op1 := buf[pc+1]
			op2 := buf[pc+2]
			dst := buf[pc+3]
			buf[dst] = buf[op1] * buf[op2]
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

	// Part 1:

	// Restore "1202 program alarm" state
	prg[1] = 12
	prg[2] = 2

	output, err := runIntCode(prg)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Part one: %d\n", output[0])

	// Part 2:
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			prg[1] = noun
			prg[2] = verb

			output, err = runIntCode(prg)

			if err != nil {
				log.Fatal(err)
			}

			if output[0] == 19690720 {
				fmt.Printf("Part two: noun=%d, verb=%d, answer=%d", noun, verb, noun*100+verb)
				break
			}
		}
	}
}
