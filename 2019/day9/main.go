package main

import (
	"fmt"
	"io/ioutil"
	"log"
)

func readInput(filename string) (source string, err error) {
	raw, err := ioutil.ReadFile(filename)

	if err != nil {
		return "", err
	}

	return string(raw), nil
}

func main() {
	var m IntCodeMachine

	example1 := "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
	prg, err := Parse(example1)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Example 1 program: ")
	fmt.Println(prg)

	m.Init(prg, []int{})
	m.Run([]int{})
	output := m.ReadOutput()
	fmt.Printf("Example 1 output:  ")
	fmt.Println(output)

	example2 := "1102,34915192,34915192,7,4,7,99,0"
	prg, err = Parse(example2)

	if err != nil {
		log.Fatal(err)
	}

	m.Init(prg, []int{})
	m.Run([]int{})
	output = m.ReadOutput()
	fmt.Print("Example 2 output: ")
	fmt.Println(output)

	example3 := "104,1125899906842624,99"
	prg, err = Parse(example3)

	if err != nil {
		log.Fatal(err)
	}

	m.Init(prg, []int{})
	m.Run([]int{})
	output = m.ReadOutput()
	fmt.Print("Example 3 output: ")
	fmt.Println(output)

	source, err := readInput("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	prg, err = Parse(source)

	if err != nil {
		log.Fatal(err)
	}

	m.Init(prg, []int{1})
	m.Run([]int{})
	output = m.ReadOutput()
	fmt.Print("Part One output: ")
	fmt.Println(output)

	m.Init(prg, []int{2})
	m.Run([]int{})
	output = m.ReadOutput()
	fmt.Print("Part Two output: ")
	fmt.Println(output)

	fmt.Println("Done!")
}
