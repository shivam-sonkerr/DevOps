package main

import (
	"fmt"
	"math"
)

func sqrt(x float64) string {
	if x < 0 {

		return sqrt(-x) + "i"
	}

	return fmt.Sprint(math.Sqrt(x))

}

func cuberoot(x float64) float64 {

	return math.Cbrt(x)

}

func pow(x, n, lim float64) float64 {

	if v := math.Pow(x, n); v < lim {

		return v
	}

	return lim
}

func main() {
	fmt.Println(sqrt(9), sqrt(-25))
	fmt.Println(cuberoot(27), cuberoot(-64))
	fmt.Println(pow(3, 2, 7))
}
