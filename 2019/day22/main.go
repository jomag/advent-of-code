package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

func dealNewStack(deck []int) []int {
	for i, j := 0, len(deck)-1; i < j; i, j = i+1, j-1 {
		deck[i], deck[j] = deck[j], deck[i]
	}
	return deck
}

func cutCards(deck []int, n int) []int {
	if n < 0 {
		n = len(deck) + n
	}
	return append(deck[n:], deck[:n]...)
}

func dealWithIncrement(deck []int, n int) []int {
	newDeck := make([]int, len(deck))
	for i := range deck {
		newDeck[i] = -1
	}

	for i := range deck {
		newDeck[(i*n)%len(deck)] = deck[i]
	}

	return newDeck
}

func newDeck(count int) []int {
	deck := make([]int, count)
	for i := range deck {
		deck[i] = i
	}
	return deck
}

func runCommands(commands string, deck []int) []int {
	lines := strings.Split(commands, "\n")
	for _, cmd := range lines {
		if len(cmd) >= 19 && cmd[:19] == "deal into new stack" {
			deck = dealNewStack(deck)
		}

		if len(cmd) > 20 && cmd[:20] == "deal with increment " {
			n, err := strconv.Atoi(cmd[20:])
			if err != nil {
				log.Fatal(err)
			}
			deck = dealWithIncrement(deck, n)
		}

		if len(cmd) > 4 && cmd[:4] == "cut " {
			n, err := strconv.Atoi(cmd[4:])
			if err != nil {
				log.Fatal(err)
			}
			deck = cutCards(deck, n)
		}
	}

	return deck
}

func main() {
	commands, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}

	deck := runCommands(string(commands), newDeck(10007))

	for i, card := range deck {
		if card == 2019 {
			fmt.Printf("Part One: position of card 2019 is %d\n", i)
			break
		}
	}
}
