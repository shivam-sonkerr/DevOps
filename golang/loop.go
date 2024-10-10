package main

import "fmt"

func addition(sum int) (x int) {
	for i := 0; i < 20; i++ {
		x = sum + i
	}
	return
}

func multiply(mult int) (y int) {

	for i := 0; i < 10; i++ {
		y = mult + (mult * i)
	}
	return

}

func main() {
	sum := 0
	for i := 0; i < 10; i++ {
		sum = sum + i
	}
	fmt.Println(sum)
	fmt.Println(multiply(5))
	fmt.Println(addition(0))
}
