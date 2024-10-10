package main

import "fmt"

func multiply(mult int) (x, y int) {

	x = mult * 4
	y = mult * 8

	return
}

func main() {
	fmt.Println(multiply(188))

}
