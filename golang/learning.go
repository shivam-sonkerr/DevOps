package main

import (
	"errors"
	"fmt"
)

//func main() {
//	var a int
//	a = 5
//	fmt.Println("Hello World")
//
//	fmt.Println(a)
//}

func divide(a, b int) (int, error) {

	if b == 0 {
		return 0, errors.New("Cannot divide by Zero")
	}
	return a / b, nil
}

func main() {

	var x int
	x = 67

	if x > 100 {
		fmt.Println("Number is greater than 100")
	} else {
		fmt.Println("Number is less than 100")
	}

	for i := 900; i < 1000; i++ {
		fmt.Println(i)
	}

	var b int = 90
	var p *int = &b

	fmt.Println(*p)

	arr := []int{1, 2, 3}
	for j := 0; j < len(arr); j++ {
		fmt.Println(arr[j])
	}

	arr1 := []float32{1.5, 5.9, 9.8}

	for k := 0; k < len(arr1); k++ {
		fmt.Println(arr1[k] / 2)
	}

	result, err := divide(81, 9)
	if err != nil {
		fmt.Println("Error", err)
		return

	}
	fmt.Println(result)
}
