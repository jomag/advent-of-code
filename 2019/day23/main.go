package main

import (
	"fmt"
	"log"
)

func main() {
	machines := make([]IntCodeMachine, 50)
	bufferts := make([][]int, 50)

	partOne := true
	natHasPacket := false
	natPacket := []int{0, 0}
	partTwoValues := make(map[int]bool)

	for i := range machines {
		err := machines[i].Load("input.txt")
		if err != nil {
			log.Fatal(err)
		}
		machines[i].blockOnInput = false
		machines[i].Input([]int{i})
	}

	for {
		for i := range machines {
			_, err := machines[i].Step()
			if err != nil {
				log.Fatal(err)
			}

			output := machines[i].ReadOutput()
			if len(output) > 0 {
				bufferts[i] = append(bufferts[i], output...)
				for len(bufferts[i]) >= 3 {
					packet := bufferts[i][:3]
					bufferts[i] = bufferts[i][3:]
					if packet[0] == 255 {
						if partOne {
							fmt.Printf("Y-value of first packet to address 255 is: %d\n", packet[2])
							partOne = false
						}
						natPacket = packet[1:]
						natHasPacket = true
					}
					if packet[0] < 50 {
						machines[packet[0]].Input(packet[1:])
					}
				}
			}
		}

		idle := true

		for i := range machines {
			if len(machines[i].inputBuffer) > 0 {
				idle = false
				break
			}
		}

		if idle && natHasPacket {
			machines[0].Input(natPacket)
			natHasPacket = false
			if _, ok := partTwoValues[natPacket[1]]; ok {
				fmt.Printf("First Y-value delivered twice to address 0 is: %d\n", natPacket[1])
				break
			}
			partTwoValues[natPacket[1]] = true
		}
	}
}
