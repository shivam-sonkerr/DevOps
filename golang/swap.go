package main

import "fmt"

func swap(x string, y string) (string, string) {
	return y, x
}

func main() {
	a, b := swap("Hi", "Hello")
	fmt.Println(a, b)
}
