package main

import (
	"fmt"
	"io"
	"os"
)

func identity(r io.Reader) (int, error) {
	fmt.Println("Enter the two numbers: ")
	var a, b int

	_, err := fmt.Fscanf(r, "%d %d", &a, &b)

	if err != nil {

		return 0, err

	}

	return a*a + b*b + 2*a*b, nil

}

func main() {

	sq, err := identity(os.Stdin)

	if err != nil {
		fmt.Println("Error", err)
		return
	}

	fmt.Println("Result: ", sq)

}
