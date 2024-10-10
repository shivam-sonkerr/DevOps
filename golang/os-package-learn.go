package main

import (
	"fmt"
	"os"
)

func main() {

	file, err := os.Open("abc.txt")

	if err != nil {

		fmt.Println("Error", err)
		return
	}

	defer file.Close()

	buffer := make([]byte, 100)
	n, err := file.Read(buffer)

	if err != nil {

		fmt.Println("Error reading file ", err)

		return

	}

	fmt.Printf("Read %d bytes: %s\n", n, buffer[:n])

}
