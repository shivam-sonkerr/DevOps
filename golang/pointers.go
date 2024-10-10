package main

import "fmt"

func main() {

	i, j := 20, 928

	p := &i
	fmt.Println(*p)

	p = &j
	*p = *p / 4
	fmt.Println(j)

}
