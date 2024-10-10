package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {

	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Enter the domain name for lookup : ")

	domain, _ := reader.ReadString('\n')

	domain = strings.TrimSpace(domain)

	address, err := net.LookupHost(domain)

	if err != nil {

		fmt.Println("Error in resolving the given domain ", err)
		return
	}

	fmt.Println("IP Addresses for", domain, " are : ")

	for _, address := range address {

		fmt.Println("  -", address)

	}

	fmt.Println("\nEnter the host for CNAME lookup")
	host, _ := reader.ReadString('\n')
	host = strings.TrimSpace(host)

	cname, err := net.LookupCNAME(host)
	txt, err := net.LookupTXT(domain)

	if err != nil {

		fmt.Println("Error in checking CNAME Records", err)
		return

	}

	fmt.Println("Canonical name for host is : ", cname)
	fmt.Println("\nTXT Records for the domain is : ", txt)
}
