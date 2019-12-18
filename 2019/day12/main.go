package main

import (
	"fmt"
)

// Moon - moon state
type Moon struct {
	name       string
	x, y, z    int
	vx, vy, vz int
}

func (moon Moon) String() string {
	return fmt.Sprintf("pos<%d, %d, %d> vel<%d, %d, %d> (%s)",
		moon.x, moon.y, moon.z,
		moon.vx, moon.vy, moon.vz,
		moon.name)
}

func abs(i int) int {
	if i < 0 {
		return -i
	}
	return i
}

func (moon Moon) potentialEnergy() int {
	return abs(moon.x) + abs(moon.y) + abs(moon.z)
}

func (moon Moon) kineticEnergy() int {
	return abs(moon.vx) + abs(moon.vy) + abs(moon.vz)
}

func (moon Moon) totalEnergy() int {
	return moon.potentialEnergy() * moon.kineticEnergy()
}

func applyGravity(moon1 *Moon, moon2 *Moon) {
	if moon1.x < moon2.x {
		moon1.vx++
		moon2.vx--
	}

	if moon1.x > moon2.x {
		moon1.vx--
		moon2.vx++
	}

	if moon1.y < moon2.y {
		moon1.vy++
		moon2.vy--
	}

	if moon1.y > moon2.y {
		moon1.vy--
		moon2.vy++
	}

	if moon1.z < moon2.z {
		moon1.vz++
		moon2.vz--
	}

	if moon1.z > moon2.z {
		moon1.vz--
		moon2.vz++
	}
}

func applyVelocity(moon *Moon) {
	moon.x += moon.vx
	moon.y += moon.vy
	moon.z += moon.vz
}

func printState(step int, moons []Moon) {
	fmt.Printf("Step %d:\n", step)
	for i := range moons {
		fmt.Printf("- %s\n", moons[i])
	}
	kinetic := 0
	potential := 0
	total := 0
	for i := range moons {
		kinetic += moons[i].kineticEnergy()
		potential += moons[i].potentialEnergy()
		total += moons[i].totalEnergy()
	}
	fmt.Printf("Kinetic: %d  Potential: %d  Total: %d\n",
		kinetic, potential, total)
}

func update(moons []Moon) {
	for i := 0; i < len(moons); i++ {
		for j := i + 1; j < len(moons); j++ {
			applyGravity(&moons[i], &moons[j])
		}
	}

	for i := range moons {
		applyVelocity(&moons[i])
	}
}

func run(moons []Moon, steps int, verbose bool) {
	if verbose {
		printState(0, moons)
		fmt.Scanln()
	}

	for step := 1; step <= steps; step++ {
		update(moons)
		if verbose {
			printState(step, moons)
			fmt.Scanln()
		}
	}

	if !verbose {
		printState(steps, moons)
	}

	fmt.Println("Done!")
}

func runUntilRepeated(moons []Moon) (steps int) {
	initial := make([]Moon, len(moons))
	copy(initial, moons)

	var stepX, stepY, stepZ int

	for step := 1; ; step++ {
		update(moons)
		eqX := true
		eqY := true
		eqZ := true
		for i := range moons {
			if moons[i].x != initial[i].x || moons[i].vx != initial[i].vx {
				eqX = false
			}
			if moons[i].y != initial[i].y || moons[i].vy != initial[i].vy {
				eqY = false
			}
			if moons[i].z != initial[i].z || moons[i].vz != initial[i].vz {
				eqZ = false
			}
		}
		if eqX && stepX == 0 {
			stepX = step
		}
		if eqY && stepY == 0 {
			stepY = step
		}
		if eqZ && stepZ == 0 {
			stepZ = step
		}
		if stepX > 0 && stepY > 0 && stepZ > 0 {
			break
		}
	}

	reps := []int{stepX, stepY, stepZ}

	biggest := int64(0)
	for i := range reps {
		if int64(reps[i]) > biggest {
			biggest = int64(reps[i])
		}
	}

	for i := int64(1); ; i++ {
		all := true
		for j := range reps {
			if (biggest*i)%int64(reps[j]) != 0 {
				all = false
				break
			}
		}
		if all {
			return int(i * biggest)
		}
	}
}

func main() {
	example1 := []Moon{
		{"Io", -1, 0, 2, 0, 0, 0},
		{"Europa", 2, -10, -7, 0, 0, 0},
		{"Ganymede", 4, -8, 8, 0, 0, 0},
		{"Callisto", 3, 5, -1, 0, 0, 0},
	}

	run(example1, 10, false)

	input := []Moon{
		{"Io", 1, 4, 4, 0, 0, 0},
		{"Europa", -4, -1, 19, 0, 0, 0},
		{"Ganymede", -15, -14, 12, 0, 0, 0},
		{"Callisto", -17, 1, 10, 0, 0, 0},
	}

	fmt.Print("\nPart One:\n\n")
	run(input, 1000, false)

	fmt.Print("\nPart two:\n\n")
	example2 := []Moon{
		{"Io", -1, 0, 2, 0, 0, 0},
		{"Europa", 2, -10, -7, 0, 0, 0},
		{"Ganymede", 4, -8, 8, 0, 0, 0},
		{"Callisto", 3, 5, -1, 0, 0, 0},
	}
	steps := runUntilRepeated(example2)
	fmt.Printf("Example: steps until repeated: %d\n", steps)

	input2 := []Moon{
		{"Io", 1, 4, 4, 0, 0, 0},
		{"Europa", -4, -1, 19, 0, 0, 0},
		{"Ganymede", -15, -14, 12, 0, 0, 0},
		{"Callisto", -17, 1, 10, 0, 0, 0},
	}
	steps = runUntilRepeated(input2)
	fmt.Printf("Steps until repeated: %d\n", steps)
}
