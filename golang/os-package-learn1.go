package main

import (
	"fmt"
	"os"
)

func main() {

	dir, err := os.Getwd()

	pid := os.Getpid()

	ppid := os.Getppid()

	uid := os.Getuid()

	if err != nil {

		fmt.Println("Error", err)

	}

	fmt.Println("Current Working directory is: ", dir)
	fmt.Println("Process ID is : ", pid)
	fmt.Println("Parent process ID is : ", ppid)
	fmt.Println("UID is : ", uid)

	return

}
