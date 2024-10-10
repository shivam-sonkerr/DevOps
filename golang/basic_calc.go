package main

import "fmt"

func add(a, b int) (sum int) {
	sum = a + b
	return
}

func multiply(a, b int) (mult int) {
	mult = a * b
	return
}

func main() {
	fmt.Println(add(8, 9))
	fmt.Println(multiply(188, 8))
}
