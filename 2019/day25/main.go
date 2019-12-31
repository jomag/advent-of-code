package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

func str2ints(str string) (out []int) {
	out = make([]int, len(str))
	for i, b := range []byte(str) {
		out[i] = int(b)
	}
	return
}

func readCommand() string {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print(">>> ")
	text, _ := reader.ReadString('\n')
	text = text[:len(text)-1]

	switch text {
	case "n":
		text = "north"
	case "s":
		text = "south"
	case "w":
		text = "west"
	case "e":
		text = "east"
	}

	return text
}

func ints2str(values []int) (out string) {
	bytes := make([]string, len(values))
	for i, b := range values {
		bytes[i] = string(b)
	}
	out = strings.Join(bytes, "")
	return
}

func bruteForceSecurity(m *IntCodeMachine) {
	items := []string{
		"space heater",
		"dark matter",
		"bowl of rice",
		"klein bottle",
		"spool of cat6",
		"manifold",
		"whirled peas",
		"antenna",
	}

	inList := func(haystack []string, needle string) bool {
		for _, value := range haystack {
			if needle == value {
				return true
			}
		}
		return false
	}

	var recurse func(with []string, without []string) bool
	tries := 0

	recurse = func (with []string, without []string) bool {
		if len(with) + len(without) == len(items) {
			for _, item := range with {
				m.Input(str2ints(fmt.Sprintf("take %s\n", item)))
			}
			for _, item := range without {
				m.Input(str2ints(fmt.Sprintf("drop %s\n", item)))
			}
			m.Run()
			m.ReadOutput()

			m.Input(str2ints("north\n"))
			m.Run()
			tries++
			output := ints2str(m.ReadOutput())

			if !strings.Contains(output, "Alert!") {
				fmt.Printf("\nFound correct inventory after %d tries!\n", tries)
				fmt.Println(output)
				return true
			}

			// fmt.Println(output)
			if tries % 1000 == 0 {
				fmt.Print(".")
			}
			return false;
		} else {

		for _, item := range items {
			if !inList(with, item) && !inList(without, item) {
				if recurse(append(with, item), without) {
					return true
				}
				if recurse(with, append(without, item)) {
					return true
				}
			}
		}
		
		return false
	}
	}
	recurse([]string{}, []string{})
}

func main() {
	var m IntCodeMachine
	err := m.Load("input.txt")
	if err != nil {
		log.Fatal(err)
	}

	m.blockOnInput = true

	for {
		m.Run()
		output := m.ReadOutput()
		fmt.Println(ints2str(output))
		inp := readCommand()
		if inp == "play script" {
			script, err := ioutil.ReadFile("script.txt")
			if err != nil {
				log.Fatal(err)
			}
			m.Input(str2ints(string(script)))		
		} else if inp == "brute force" {
			bruteForceSecurity(&m)
		} else {
			m.Input(str2ints(inp + "\n"))
		}
	}
}
