package main

import (
	"fmt"
	"time"
)

func just(d chan string) {

	date := <-d

	fmt.Println("Date of today is : ", date)

}

func main() {

	d := make(chan string)

	go just(d)

	d <- time.Now().String()

	close(d)

}
