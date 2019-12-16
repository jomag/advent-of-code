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

// IntCodeMachine state of machine
type IntCodeMachine struct {
	pc           int
	stopped      bool
	memory       []int
	inputBuffer  []int
	outputBuffer []int
}

func createMachine(program []int, input []int) (machine IntCodeMachine) {
	buf := make([]int, len(program))
	copy(buf[:], program)

	return IntCodeMachine{
		0,
		false,
		buf,
		input,
		[]int{},
	}
}

func run(machine *IntCodeMachine, input []int) (err error) {
	machine.inputBuffer = append(machine.inputBuffer, input...)
	buf := machine.memory
	pc := &machine.pc

	for {
		if buf[*pc] == OpHalt {
			machine.stopped = true
			break
		}

		// fmt.Printf("Next: %d (@%d)\n", buf[pc], pc)

		switch buf[*pc] % 100 {
		case OpAdd:
			op1 := readParameter(0, buf, *pc)
			op2 := readParameter(1, buf, *pc)
			dst := buf[*pc+3]
			buf[dst] = op1 + op2
			*pc += 4
		case OpMul:
			op1 := readParameter(0, buf, *pc)
			op2 := readParameter(1, buf, *pc)
			dst := buf[*pc+3]
			buf[dst] = op1 * op2
			*pc += 4
		case OpInput:
			dst := buf[*pc+1]
			if len(machine.inputBuffer) > 0 {
				buf[dst], machine.inputBuffer = machine.inputBuffer[0], machine.inputBuffer[1:]
				*pc += 2
			} else {
				// Blocked on input
				return nil
			}
		case OpOutput:
			op1 := readParameter(0, buf, *pc)
			machine.outputBuffer = append(machine.outputBuffer, op1)
			*pc += 2
		case OpJumpIfTrue:
			op1 := readParameter(0, buf, *pc)
			op2 := readParameter(1, buf, *pc)
			if op1 != 0 {
				*pc = op2
			} else {
				*pc += 3
			}
		case OpJumpIfFalse:
			op1 := readParameter(0, buf, *pc)
			op2 := readParameter(1, buf, *pc)
			if op1 == 0 {
				*pc = op2
			} else {
				*pc += 3
			}
		case OpLess:
			op1 := readParameter(0, buf, *pc)
			op2 := readParameter(1, buf, *pc)
			dst := buf[*pc+3]
			if op1 < op2 {
				buf[dst] = 1
			} else {
				buf[dst] = 0
			}
			*pc += 4
		case OpEqual:
			op1 := readParameter(0, buf, *pc)
			op2 := readParameter(1, buf, *pc)
			dst := buf[*pc+3]
			if op1 == op2 {
				buf[dst] = 1
			} else {
				buf[dst] = 0
			}
			*pc += 4
		default:
			return fmt.Errorf("Invalid operator '%d' at index %d", buf[*pc], *pc)
		}

		if *pc >= len(buf) {
			return fmt.Errorf("Reached end of code")
		}
	}

	return nil
}

func readInput(filename string) (source string, err error) {
	raw, err := ioutil.ReadFile(filename)

	if err != nil {
		return "", err
	}

	return string(raw), nil
}

func parse(source string) (program []int, err error) {
	nums := strings.Split(source, ",")
	code := make([]int, len(nums))
	for i, num := range nums {
		code[i], err = strconv.Atoi(strings.TrimSpace(num))
		if err != nil {
			return nil, err
		}
	}

	return code, nil
}

func runSequence(prg []int, phaseSettings []int) (signal int, err error) {
	output := 0

	for i := range phaseSettings {
		m := createMachine(prg, []int{})
		err = run(&m, []int{phaseSettings[i], output})
		if err != nil {
			return 0, err
		}
		output = m.outputBuffer[0]
	}

	return output, nil
}

func runSequencePart2(prg []int, phaseSettings []int) (signal int, err error) {
	count := len(phaseSettings)
	var machines []IntCodeMachine

	for i := 0; i < count; i++ {
		machines = append(machines, createMachine(prg, []int{phaseSettings[i]}))
	}

	outp := 0
	for {
		for i := range machines {
			machine := &machines[i]
			err = run(machine, []int{outp})
			if err != nil {
				return 0, err
			}
			outp = machine.outputBuffer[0]
			machine.outputBuffer = machine.outputBuffer[1:]
		}

		if machines[len(machines)-1].stopped {
			break
		}
	}

	return outp, nil
}

func permutations(inp []int) [][]int {
	if len(inp) == 1 {
		return [][]int{{inp[0]}}
	}

	var result [][]int

	for i, c := range inp {
		rest := append(inp[i+1:], inp[:i]...)
		for _, permutation := range permutations(rest) {
			result = append(result, append([]int{c}, permutation...))
		}
	}

	return result
}

func main() {
	examples := []string{
		"3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",
		"3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
		"3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
	}

	examplePhaseSettings := [][]int{
		{4, 3, 2, 1, 0},
		{0, 1, 2, 3, 4},
		{1, 0, 4, 3, 2},
	}

	for i, example := range examples {
		prg, err := parse(example)

		if err != nil {
			log.Fatal(err)
		}

		signal, err := runSequence(prg, examplePhaseSettings[i])

		if err != nil {
			log.Fatal(err)
		}

		fmt.Printf("Final output: %d\n", signal)
	}

	source, err := readInput("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	prg, err := parse(source)

	if err != nil {
		log.Fatal(err)
	}

	highest := 0
	var highestPhaseSettings []int

	options := permutations([]int{0, 1, 2, 3, 4})
	for _, opt := range options {
		signal, err := runSequence(prg, opt)

		if err != nil {
			log.Fatal(err)
		}

		if signal > highest {
			highest = signal
			highestPhaseSettings = opt
		}
	}

	fmt.Println("Part One:")
	fmt.Printf("Highest thruster signal: %d\n", highest)
	fmt.Println(highestPhaseSettings)

	// Part Two

	examplesPartTwo := []string{
		"3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
		"3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
	}

	examplePhaseSettingsPartTwo := [][]int{
		{9, 8, 7, 6, 5},
		{9, 7, 8, 5, 6},
	}

	for i, example := range examplesPartTwo {
		prg, err := parse(example)

		if err != nil {
			log.Fatal(err)
		}

		signal, err := runSequencePart2(prg, examplePhaseSettingsPartTwo[i])

		if err != nil {
			log.Fatal(err)
		}

		fmt.Printf("Final output: %d\n", signal)
	}

	options = permutations([]int{5, 6, 7, 8, 9})
	highest = 0

	for _, opt := range options {
		signal, err := runSequencePart2(prg, opt)

		if err != nil {
			log.Fatal(err)
		}

		if signal > highest {
			highest = signal
			highestPhaseSettings = opt
		}
	}

	fmt.Printf("Highest thruster signal: %d\n", highest)
	fmt.Println(highestPhaseSettings)
}
