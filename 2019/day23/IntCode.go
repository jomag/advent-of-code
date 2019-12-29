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
	// OpJumpNotZero - Jump if true
	OpJumpNotZero = 5
	// OpJumpZero - Jump if false
	OpJumpZero = 6
	// OpLess - Set true if op 1 < op 2
	OpLess = 7
	// OpEqual - Set true if op 1 == op2
	OpEqual = 8
	// OpAddToRelativeBase - Add op1 to relative base
	OpAddToRelativeBase = 9
	// OpHalt - Halt operator
	OpHalt = 99
)

const (
	minMemorySize = 8192
)

// IntCodeMachine state of machine
type IntCodeMachine struct {
	pc           int
	stopped      bool
	debug        bool
	blockOnInput bool
	relativeBase int
	program      []int
	memory       []int
	inputBuffer  []int
	outputBuffer []int
}

// Max - Return max of two int values
func Max(a, b int) int {
	if a > b {
		return a
	}

	return b
}

// Init - Initialize machine with a program and input buffer
func (m *IntCodeMachine) Init(program []int, input []int) {
	m.pc = 0
	m.stopped = false
	m.debug = false
	m.relativeBase = 0
	m.program = make([]int, len(program))
	m.memory = make([]int, Max(len(program), minMemorySize))
	copy(m.program[:], program)
	copy(m.memory[:], program)
	m.inputBuffer = input
}

func getParameterMode(op int, param int) int {
	switch param {
	case 0:
		return op / 100 % 10
	case 1:
		return op / 1000 % 10
	case 2:
		return op / 10000 % 10
	default:
		log.Fatal("Only 3 parameters supported")
		return -1
	}
}

func getModeName(mode int) string {
	switch mode {
	case 0:
		return "positional"
	case 1:
		return "immediate"
	case 2:
		return "relative"
	default:
		return "illegal mode"
	}
}

func getOpName(op int) string {
	switch op % 100 {
	case OpAdd:
		return "ADD "
	case OpMul:
		return "MUL "
	case OpInput:
		return "INP "
	case OpOutput:
		return "OUT "
	case OpJumpNotZero:
		return "JNZ "
	case OpJumpZero:
		return "JZ  "
	case OpLess:
		return "LESS"
	case OpEqual:
		return "EQ  "
	case OpAddToRelativeBase:
		return "ARB "
	case OpHalt:
		return "HALT"
	default:
		return "Illegal Op"
	}
}

func (m *IntCodeMachine) writeParameter(param int, offs int, value int) {
	op := m.memory[offs]
	mode := getParameterMode(op, param)
	addr := m.memory[offs+param+1]

	switch mode {
	case 0:
		m.memory[addr] = value
	case 2:
		m.memory[m.relativeBase+addr] = value
	default:
		log.Fatal("Illegal mode for write parameter")
	}
}

func (m *IntCodeMachine) readParameter(param int, offs int) (val int) {
	op := m.memory[offs]
	mode := getParameterMode(op, param)
	addr := m.memory[offs+param+1]

	switch mode {
	case 0:
		// Position mode
		val = m.memory[addr]

	case 1:
		// Immediate mode
		val = addr

	case 2:
		// Relative mode
		val = m.memory[m.relativeBase+addr]

	default:
		log.Fatal("Illegal mode")
	}

	if m.debug {
		fmt.Printf("- Param %d: mode %d %s, value %d\n", param, mode, getModeName(mode), val)
	}

	return
}

// Reset machine. Memory is reset and program will restart from 0.
func (m *IntCodeMachine) Reset() {
	m.pc = 0
	m.stopped = false
	m.debug = false
	m.relativeBase = 0
	m.inputBuffer = []int{}
	m.outputBuffer = []int{}
	copy(m.memory[:], m.program)
}

// Input - Append data to input buffer
func (m *IntCodeMachine) Input(input []int) {
	m.inputBuffer = append(m.inputBuffer, input...)
}

// Step - Run a single instruction
func (m *IntCodeMachine) Step() (blocked bool, err error) {
	op := m.memory[m.pc]

	if m.debug {
		fmt.Printf("Op %d: %s. Rel base: %d\n", op, getOpName(op), m.relativeBase)
	}

	if op == OpHalt {
		m.stopped = true
		return false, nil
	}

	// fmt.Printf("Next: %d (@%d)\n", buf[pc], pc)

	switch op % 100 {
	case OpAdd:
		op1 := m.readParameter(0, m.pc)
		op2 := m.readParameter(1, m.pc)
		m.writeParameter(2, m.pc, op1+op2)
		m.pc += 4

	case OpMul:
		op1 := m.readParameter(0, m.pc)
		op2 := m.readParameter(1, m.pc)
		m.writeParameter(2, m.pc, op1*op2)
		m.pc += 4

	case OpInput:
		if len(m.inputBuffer) > 0 {
			var val int
			val, m.inputBuffer = m.inputBuffer[0], m.inputBuffer[1:]
			m.writeParameter(0, m.pc, val)
			m.pc += 2
		} else if !m.blockOnInput {
			m.writeParameter(0, m.pc, -1)
			m.pc += 2
		} else {
			return true, nil
		}

	case OpOutput:
		op1 := m.readParameter(0, m.pc)
		m.outputBuffer = append(m.outputBuffer, op1)
		m.pc += 2

	case OpJumpNotZero:
		op1 := m.readParameter(0, m.pc)
		op2 := m.readParameter(1, m.pc)
		if op1 != 0 {
			m.pc = op2
		} else {
			m.pc += 3
		}

	case OpJumpZero:
		op1 := m.readParameter(0, m.pc)
		op2 := m.readParameter(1, m.pc)
		if op1 == 0 {
			m.pc = op2
		} else {
			m.pc += 3
		}

	case OpLess:
		op1 := m.readParameter(0, m.pc)
		op2 := m.readParameter(1, m.pc)
		if op1 < op2 {
			m.writeParameter(2, m.pc, 1)
		} else {
			m.writeParameter(2, m.pc, 0)
		}
		m.pc += 4

	case OpEqual:
		op1 := m.readParameter(0, m.pc)
		op2 := m.readParameter(1, m.pc)
		if op1 == op2 {
			m.writeParameter(2, m.pc, 1)
		} else {
			m.writeParameter(2, m.pc, 0)
		}
		m.pc += 4

	case OpAddToRelativeBase:
		op1 := m.readParameter(0, m.pc)
		m.relativeBase += op1
		m.pc += 2

	default:
		return false, fmt.Errorf("Invalid operator '%d' at index %d", m.memory[m.pc], m.pc)
	}

	if m.pc >= len(m.memory) {
		return false, fmt.Errorf("Reached end of code")
	}

	return false, nil
}

// Run - Run machine until stopped or blocked
func (m *IntCodeMachine) Run() (err error) {
	for {
		blocked, err := m.Step()
		if err != nil {
			return err
		}
		if blocked || m.stopped {
			return nil
		}
	}
}

// ReadOutput - return all output from machine and clear output buffer
func (m *IntCodeMachine) ReadOutput() (output []int) {
	output = m.outputBuffer
	m.outputBuffer = []int{}
	return output
}

// Parse - Parse IntCode into array of ints
func Parse(source string) (program []int, err error) {
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

// Load program from file
func (m *IntCodeMachine) Load(filename string) error {
	src, err := ioutil.ReadFile(filename)

	if err != nil {
		return err
	}

	prg, err := Parse(string(src))

	if err != nil {
		return err
	}

	m.Init(prg, []int{})

	return nil
}
