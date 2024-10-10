package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"

	"github.com/ipinfo/go/v2/ipinfo"
)

func main() {
	token := os.Getenv("API_TOKEN")

	client := ipinfo.NewClient(nil, nil, token)

	const ip_address = "1.1.1.1"

	info, err := client.GetIPInfo(net.ParseIP(ip_address))

	if err != nil {

		log.Fatal(err)
	}

	cmd := exec.Command("curl", "ipinfo.io/ip")
	output, err := cmd.Output()

	if err != nil {
		log.Fatal(err)

	}

	ip_addr := string(output)

	ownIPInfo, err := ipinfo.GetIPInfo(net.ParseIP(ip_addr))

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("*************************************************************IP INFO API******************************************************")
	fmt.Println("\n\n")
	fmt.Println("Your IP Address : \n", ip_addr)
  
	fmt.Println("\n\n")
	fmt.Println("Details of your IP : \n\n", ownIPInfo)

	fmt.Println("\n")

	fmt.Println("Structured Information: \n")

	fmt.Println(" IP Address: ", ownIPInfo.IP)
	fmt.Println(" Country Name: ", ownIPInfo.CountryName)
	fmt.Println(" Country Code: ", ownIPInfo.Country)
	fmt.Println(" City:  ", ownIPInfo.City)
	fmt.Println(" Region: ", ownIPInfo.Region)
	fmt.Println(" Hostname: ", ownIPInfo.Hostname)
	fmt.Println(" Coordinates: ", ownIPInfo.Location)
	fmt.Println(" Continent: ", ownIPInfo.Continent.Name)
	fmt.Println(" Continent Code: ", ownIPInfo.Continent.Code)
	fmt.Println(" Organization: ", ownIPInfo.Org)
	fmt.Println(" Timezone: ", ownIPInfo.Timezone)

	fmt.Println("\n\n")
	fmt.Println("-------------------------------------")
	fmt.Println("Details of Cloudflare DNS IP : ", ip_address)
	fmt.Println("-------------------------------------")
	fmt.Println("\n\n")
	fmt.Println(info)
	fmt.Println("\n\n")
	fmt.Println("Structured Information: \n")
	fmt.Println(" IP Address: ", info.IP)
	fmt.Println(" Country Name: ", info.CountryName)
	fmt.Println(" Country Code: ", info.Country)
	fmt.Println(" City:  ", info.City)
	fmt.Println(" Region: ", info.Region)
	fmt.Println(" Hostname: ", info.Hostname)
	fmt.Println(" Coordinates: ", info.Location)
	fmt.Println(" Continent: ", info.Continent.Name)
	fmt.Println(" Continent Code: ", info.Continent.Code)
	fmt.Println(" Organization: ", info.Org)
  fmt.Println(" Timezone: ", info.Timezone)
  fmt.Println()
}
