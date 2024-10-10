package main

import (
	"fmt"
	"io"
	"os"
)

func multiply(r io.Reader) (int, error) {

	fmt.Println("Enter two numbers to multiply")

	var a, b int

	_, err := fmt.Fscanf(r, "%d %d", &a, &b)

	if err != nil {

		return 0, err

	}

	return a * b, nil

}

func main() {

	mult, err := multiply(os.Stdin)

	if err != nil {

		fmt.Println("Error", err)

		return
	}

	fmt.Println("Result : ", mult)

}
