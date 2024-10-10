package main

import (
	"fmt"
	"io"
	"net"
)

func main() {

	listener, err := net.Listen("tcp", ":8080")

	if err != nil {
		fmt.Println("Error in creating listener", err)
		return
	}

	defer listener.Close()

	fmt.Println("Listening on port  :8080...")

	for {

		conn, err := listener.Accept()

		if err != nil {
			fmt.Println("Error in accepting connection ", err)

			continue
		}

		go handleConnection(conn)

	}

}

func handleConnection(conn net.Conn) {

	defer conn.Close()

	fmt.Println("New Connection From : ", conn.RemoteAddr())

	if _, err := io.Copy(conn, conn); err != nil {

		fmt.Println("Error echoing data ", err)

	}
}
