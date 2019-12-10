package main

import "testing"

func TestFuelRequired(t *testing.T) {
	tests := []struct{ mass, fuel int }{
		{12, 2},
		{14, 2},
		{1969, 654},
		{100756, 33583},
	}

	for i := 0; i < len(tests); i++ {
		fuel := FuelRequired(tests[i].mass)
		if fuel != tests[i].fuel {
			t.Errorf("Expected fuel %d when mass %d, got %d", tests[i].fuel, tests[i].mass, fuel)
		}
	}
}
