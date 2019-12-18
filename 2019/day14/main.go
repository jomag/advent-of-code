package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"strconv"
	"strings"
)

const exampleInput1 = `
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
`

const exampleInput2 = `
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
`

const exampleInput3 = `
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
`

const exampleInput4 = `
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
`

const exampleInput5 = `
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
`

// Ingredient - name of a chemical and its quantity
type Ingredient struct {
	qty  int
	name string
}

// Reaction - rule for creating chemical from a number input chemicals
type Reaction struct {
	inputs []Ingredient
	output Ingredient
}

func (r Reaction) String() (str string) {
	inputStrings := make([]string, len(r.inputs))
	for i := range r.inputs {
		inputStrings[i] = fmt.Sprintf("%d %s", r.inputs[i].qty, r.inputs[i].name)
	}
	return fmt.Sprintf("%s => %d %s", strings.Join(inputStrings, ", "), r.output.qty, r.output.name)
}

func parse(text string) (reactions []Reaction, err error) {
	lines := strings.Split(text, "\n")
	for _, line := range lines {
		var ingredients []Ingredient
		trimmed := strings.TrimSpace(line)
		if len(trimmed) > 0 {
			tmp := strings.Split(trimmed, "=>")
			inputs := strings.Split(tmp[0], ",")
			for _, input := range inputs {
				tmp := strings.Split(strings.TrimSpace(input), " ")
				qty, err := strconv.Atoi(tmp[0])
				if err != nil {
					return nil, err
				}
				ingredients = append(ingredients, Ingredient{qty, tmp[1]})
			}

			s := strings.Split(strings.TrimSpace(tmp[1]), " ")
			qty, err := strconv.Atoi(s[0])
			if err != nil {
				return nil, err
			}

			reactions = append(reactions, Reaction{ingredients, Ingredient{qty, s[1]}})
		}
	}

	return reactions, nil
}

func findReactionWithOutput(reactions []Reaction, name string) *Reaction {
	for _, r := range reactions {
		if r.output.name == name {
			return &r
		}
	}
	return nil
}

// Stock - consumed and total amount of a chemical
type Stock struct {
	consumed int
	total    int
}

func addToBom(chemical string, qty int, reactions []Reaction, bom map[string]Stock) {
	if chemical == "ORE" {
		stock := bom[chemical]
		bom[chemical] = Stock{stock.consumed + qty, stock.total + qty}
		return
	}

	stock := bom[chemical]
	available := stock.total - stock.consumed
	required := qty

	if available >= qty {
		stock.consumed += qty
		required = 0
	} else {
		stock.consumed = stock.total
		required = qty - available
	}

	reaction := findReactionWithOutput(reactions, chemical)

	n := int(math.Ceil(float64(required) / float64(reaction.output.qty)))
	stock.consumed += required
	stock.total += reaction.output.qty * n

	bom[chemical] = stock

	for _, inp := range reaction.inputs {
		addToBom(inp.name, inp.qty*n, reactions, bom)
	}
}

func runPartOne(inp string, fuel int, expected int) (err error) {
	reactions, err := parse(inp)
	if err != nil {
		return err
	}

	bom := make(map[string]Stock)

	addToBom("FUEL", fuel, reactions, bom)

	fmt.Printf("To produce %d FUEL, we need:\n", fuel)
	for k, v := range bom {
		isOre := ""
		if k == "ORE" {
			isOre = " <-----"
		}
		fmt.Printf(" - %d %s (%d consumed)%s\n", v.total, k, v.consumed, isOre)
	}

	if expected != 0 {
		fmt.Printf("Expected amount of ORE: %d\n", expected)
	}

	return nil
}

func runPartTwo(inp string, ore int) (fuel int, err error) {
	reactions, err := parse(inp)
	if err != nil {
		return 0, err
	}

	for fuel = 1; ; fuel += 100000 {
		bom := make(map[string]Stock)
		addToBom("FUEL", fuel, reactions, bom)
		if bom["ORE"].total > ore {
			for ; ; fuel -= 1000 {
				bom := make(map[string]Stock)
				addToBom("FUEL", fuel, reactions, bom)
				if bom["ORE"].total < ore {
					for ; ; fuel++ {
						bom := make(map[string]Stock)
						addToBom("FUEL", fuel, reactions, bom)
						if bom["ORE"].total >= ore {
							return fuel - 1, nil
						}
					}
				}
			}
		}
	}
}

func main() {
	raw, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal(err)
	}

	puzzleInput := string(raw)

	fmt.Print("Part One\n========\n")

	examples := []struct {
		name      string
		data      string
		printData bool
		expected  int
	}{
		{"Example 1", exampleInput1, true, 31},
		{"Example 2", exampleInput2, true, 165},
		{"Example 3", exampleInput3, true, 13312},
		{"Example 4", exampleInput4, true, 180697},
		{"Example 5", exampleInput5, true, 2210736},
		{"Puzzle Input", puzzleInput, false, 0},
	}

	for _, ex := range examples {
		fmt.Printf("\n%s\n%s\n", ex.name, strings.Repeat("-", len(ex.name)))
		if ex.printData {
			fmt.Println(strings.TrimSpace(ex.data))
			fmt.Println()
		}
		err := runPartOne(ex.data, 1, ex.expected)
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Print("\n\nPart Two\n========\n\n")
	for _, ex := range examples {
		fuel, err := runPartTwo(ex.data, 1000000000000)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%s (%d): %d units of FUEL can be produced.\n", ex.name, ex.expected, fuel)
	}
	fmt.Println("Done!")
}
