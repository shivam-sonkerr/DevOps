package main

import "fmt"

func main() {

	evens := [5]int{2, 4, 6, 8, 10}
	var e []int = evens[1:3]
	fmt.Println(e)

}
