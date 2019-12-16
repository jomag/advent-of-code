package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

// LoadImage loads an image and return an array of layers
func LoadImage(data string, width int, height int) (layers [][]int, err error) {
	for i := 0; i < len(data); i += width * height {
		str := data[i : i+width*height]
		var layer []int
		for j := 0; j < len(str); j++ {
			n, err := strconv.Atoi(str[j : j+1])
			if err != nil {
				return nil, err
			}
			layer = append(layer, n)
		}
		layers = append(layers, layer)
	}
	return layers, nil
}

func readInput(filename string) (data string, err error) {
	raw, err := ioutil.ReadFile(filename)

	if err != nil {
		return "", err
	}

	return string(raw), nil
}

func countDigitsInLayer(layer []int, digit int) (count int) {
	for i := range layer {
		if layer[i] == digit {
			count++
		}
	}
	return count
}

func findLayerWithFewest(layers [][]int, digit int) (layer []int) {
	least := -1
	for _, l := range layers {
		count := countDigitsInLayer(l, digit)
		if least < 0 || count < least {
			least = count
			layer = l
		}
	}

	return layer
}

func renderImage(layers [][]int, width int, height int) {
	const (
		TRANSP = "/"
		BLACK  = " "
		WHITE  = "8"
	)

	buf := make([]string, width*height)
	for i := range buf {
		buf[i] = TRANSP
	}

	for layerIndex := 0; layerIndex < len(layers); layerIndex++ {
		for y := 0; y < height; y++ {
			for x := 0; x < width; x++ {
				if buf[y*width+x] == TRANSP {
					c := layers[layerIndex][y*width+x]
					if c == 0 {
						buf[y*width+x] = BLACK
					}
					if c == 1 {
						buf[y*width+x] = WHITE
					}
				}
			}
		}
	}

	for y := 0; y < height; y++ {
		fmt.Println(strings.Join(buf[y*width:(y+1)*width], ""))
	}
}

func main() {
	fmt.Print("Part one:\n")
	layers, err := LoadImage("123456789012", 3, 2)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Example output: ", layers)

	inputData, err := readInput("input.txt")

	if err != nil {
		log.Fatal(err)
	}

	layers, err = LoadImage(inputData, 25, 6)
	layer := findLayerWithFewest(layers, 0)
	ones := countDigitsInLayer(layer, 1)
	twos := countDigitsInLayer(layer, 2)
	fmt.Printf("#1 * #2 = %d\n", ones*twos)

	fmt.Print("\nPart two:\n")
	renderImage(layers, 25, 6)

	fmt.Println("Done!")
}
