package main

import (
	"bufio"
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
	"strings"
)

// FuelRequired returns fuel required to launch module with given mass
func FuelRequired(mass int) int {
	return int(math.Floor(float64(mass)/3.0) - 2)
}

// FuelRequiredPartTwo returns fuel required to launch module with given
// mass plus fuel
func FuelRequiredPartTwo(mass int) int {
	var fuel int
	var f int = mass
	for {
		f = FuelRequired(f)
		if f <= 0 {
			break
		}
		fuel += f
	}

	return fuel
}

func readInput(filename string) (data []int, err error) {
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

		num, err := strconv.Atoi(strings.TrimSpace(line))

		if err != nil {
			return nil, err
		}

		data = append(data, num)
	}

	if err != io.EOF {
		return nil, err
	}

	return data, nil
}

func main() {
	input, err := readInput("input.txt")

	if err != nil {
		fmt.Println(err)
		return
	}

	var sum int
	for _, mass := range input {
		sum += FuelRequired(mass)
	}

	fmt.Println(sum)

	var sum2 int
	for _, mass := range input {
		sum2 += FuelRequiredPartTwo(mass)
	}

	fmt.Println(sum2)
}
