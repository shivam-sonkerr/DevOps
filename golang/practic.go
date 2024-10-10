package main

import (
	"errors"
	"fmt"
	"io"
	"os"
)

func division(r io.Reader) (float64, error) {

	fmt.Println("Enter the numbers for division : ")

	var a, b float64

	_, err := fmt.Fscanf(r, "%f %f", &a, &b)

	if b == 0 {
		return 0, errors.New("Division by Zero....Erroring out")
	}

	if err != nil {

		return 0, err

	}

	return a / b, nil
}

func main() {

	div, err := division(os.Stdin)

	if err != nil {

		fmt.Println("Error", err)
		return
	}

	fmt.Println("Result of division: ", div)

}
