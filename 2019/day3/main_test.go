package main

import (
	"testing"
)

func TestParseSegments(t *testing.T) {
	tests := []struct {
		src    string
		expect []Segment
	}{
		{
			"U1,D100, L32 , R93",
			[]Segment{
				{'U', 1},
				{'D', 100},
				{'L', 32},
				{'R', 93},
			},
		},
	}

	for _, test := range tests {
		result, err := ParseSegments(test.src)

		if err != nil {
			t.Error(err)
		}

		if len(result) != len(test.expect) {
			t.Errorf("Expected %d segments, got %d", len(test.expect), len(result))
			return
		}

		for j, expect := range test.expect {
			if expect.dir != result[j].dir {
				t.Errorf("Expected direction %c, got %c", expect.dir, result[j].dir)
				return
			}

			if expect.length != result[j].length {
				t.Errorf("Expected length %d, got %d", expect.length, result[j].length)
				return
			}
		}
	}
}

func TestFindClosestIntersection(t *testing.T) {
	tests := []struct {
		path1, path2 string
		closest      int
		shortest     int
	}{
		{
			"R8,U5,L5,D3",
			"U7,R6,D4,L4",
			6,
			30,
		},
		{
			"R75,D30,R83,U83,L12,D49,R71,U7,L72",
			"U62,R66,U55,R34,D71,R55,D58,R83",
			159,
			610,
		},
		{
			"R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
			"U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
			135,
			410,
		},
	}

	for _, test := range tests {
		path1, _ := ParseSegments(test.path1)
		path2, _ := ParseSegments(test.path2)
		closest, shortest := findClosestIntersection(path1, path2)
		if closest != test.closest {
			t.Errorf("Expected distance %d, got %d", test.closest, closest)
		}
		if shortest != test.shortest {
			t.Errorf("Expected length %d, got %d", test.shortest, shortest)
		}
	}
}
