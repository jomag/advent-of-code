package main

import "fmt"

func main() {
	start := 235741
	stop := 706948
	countPart1 := 0
	countPart2 := 0

	for i := start; i <= stop; i++ {
		digits := [6]int{
			(i / 100000) % 10,
			(i / 10000) % 10,
			(i / 1000) % 10,
			(i / 100) % 10,
			(i / 10) % 10,
			i % 10,
		}

		fail := false
		fail = fail || digits[0] > digits[1]
		fail = fail || digits[1] > digits[2]
		fail = fail || digits[2] > digits[3]
		fail = fail || digits[3] > digits[4]
		fail = fail || digits[4] > digits[5]

		if digits[0] != digits[1] && digits[1] != digits[2] && digits[2] != digits[3] && digits[3] != digits[4] && digits[4] != digits[5] {
			fail = true
		}

		if !fail {
			countPart1++
		}

		passSecondRule := false
		for j := 1; j < 6; j++ {
			if digits[j-1] == digits[j] {
				if (j == 1 || digits[j-2] != digits[j]) && (j == 5 || digits[j+1] != digits[j]) {
					passSecondRule = true
				}
			}
		}

		if !fail && passSecondRule {
			countPart2++
		}
	}

	fmt.Println(countPart1)
	fmt.Println(countPart2)
}
