package main

import (
	"fmt"
	"io"
	"net"
	"strings"
)

func main() {

	conn, err := net.Dial("tcp", "localhost:8080")

	if err != nil {

		fmt.Println(" Error connecting to server ", err)
		return
	}

	defer conn.Close()

	fmt.Println("Connected to the server ")

	data := "Hello , server! "

	if _, err := io.Copy(conn, strings.NewReader(data)); err != nil {

		fmt.Println("Error sending data", err)

		return

	}

	buf := make([]byte, len(data))

	if _, err := io.ReadFull(conn, buf); err != nil {

		fmt.Println("Error reading data")

		return
	}

	fmt.Println("Received from Server : ", string(buf))

}
