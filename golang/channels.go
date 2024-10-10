package main

import "fmt"

func greet(c chan string) {

	name := <-c

	fmt.Println("Hello", name)

}

func main() {

	c := make(chan string)

	go greet(c)

	c <- "World"

	close(c)

}
