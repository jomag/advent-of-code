package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

func str2ints(str string) (out []int) {
	out = make([]int, len(str))
	for i, b := range []byte(str) {
		out[i] = int(b)
	}
	return
}

func ints2str(values []int) (out string) {
	bytes := make([]string, len(values))
	for i, b := range values {
		bytes[i] = string(b)
	}
	out = strings.Join(bytes, "")
	return
}

func run(filename string) {
	var m IntCodeMachine
	m.Load("input.txt")

	raw, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}

	// Read SpringCode program and remove comments
	lines := strings.Split(string(raw), "\n")
	var code string
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		pos := strings.Index(trimmed, ";")
		if pos >= 0 {
			trimmed = trimmed[:pos]
		}
		if len(trimmed) > 0 {
			code = code + trimmed + "\n"
		}
	}

	fmt.Println("--- PROGRAM ---")
	fmt.Print(code)
	fmt.Print("--- END OF PROGRAM ---\n\n")

	m.Run(str2ints(string(code)))
	output := m.ReadOutput()

	if len(output) == 34 {
		fmt.Printf("Success! hull damage: %d\n", output[33])
	} else {
		fmt.Println(ints2str(output))
	}
}

func main() {
	fmt.Print("Part One\n========\n\n")
	run("script1.txt")

	fmt.Print("\n\nPart Two\n========\n\n")
	run("script2.txt")
}
