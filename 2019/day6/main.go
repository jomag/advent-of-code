package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func readInput(filename string) (data [][]string, err error) {
	file, err := os.Open("input.txt")
	defer file.Close()

	if err != nil {
		return nil, err
	}

	reader := bufio.NewReader(file)

	var line string
	for {
		line, err = reader.ReadString('\n')

		if err != nil {
			break
		}

		parts := strings.Split(strings.TrimSpace(line), ")")
		data = append(data, parts[0:2])
	}

	if err != io.EOF {
		return nil, err
	}

	return data, nil
}

// Object contains information about one object in space
type Object struct {
	id       string
	children []Object
}

func buildTreeRec(id string, parentMap map[string][]string) Object {
	var children []Object
	for _, childID := range parentMap[id] {
		children = append(children, buildTreeRec(childID, parentMap))
	}

	return Object{
		id,
		children,
	}
}

func buildTree(orbits [][]string) Object {
	parentMap := make(map[string][]string)

	for _, orbit := range orbits {
		parentMap[orbit[0]] = append(parentMap[orbit[0]], orbit[1])
	}

	return buildTreeRec("COM", parentMap)
}

func getOrbitCount(root Object, depth int) int {
	sum := depth

	for _, child := range root.children {
		sum += getOrbitCount(child, depth+1)
	}

	return sum
}

func findPath(root Object, id string) (path []string, found bool) {
	if root.id == id {
		return []string{id}, true
	}

	for _, child := range root.children {
		p, found := findPath(child, id)
		if found {
			return append([]string{root.id}, p...), true
		}
	}

	return nil, false
}

func main() {
	data, err := readInput("input.txt")

	if err != nil {
		fmt.Println(err)
		return
	}

	root := buildTree(data)
	orbitCount := getOrbitCount(root, 0)
	fmt.Println(orbitCount)

	santaPath, found := findPath(root, "SAN")

	if !found {
		fmt.Println("Path to SAN not found")
		return
	}

	youPath, found := findPath(root, "YOU")

	if !found {
		fmt.Println("Path to YOU not found")
		return
	}

	var i int
	for i = 0; i < len(santaPath) && i < len(youPath) && santaPath[i] == youPath[i]; i++ {
	}

	fmt.Println(len(santaPath) + len(youPath) - i - i - 2)
}
