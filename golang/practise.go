package main

import (
	"fmt"
	"io"
	"os"
)

func add(r io.Reader) (int, error) {

	fmt.Println(" Enter two numbers seperated by space: ")

	var a, b int

	_, err := fmt.Fscanf(r, "%d %d", &a, &b)

	if err != nil {

		return 0, err

	}

	return a + b, nil
}

func main() {
	sum, err := add(os.Stdin)
	if err != nil {
		fmt.Println("Error", err)
		return
	}

	fmt.Println("Sum ", sum)
}
