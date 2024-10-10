package main

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"os"
	"strconv"
)

type config struct {
	numtimes   int
	printUsage bool
}

var usageString = fmt.Sprintf(`Usage: %s <integer> [-h|--help]
A greeter application which prints the name you entered <integer> number
of times.
`, os.Args[0])

func printUsage(w io.Writer) {
	fmt.Fprintf(w, usageString)
}

func validateArguments(c config) error {
	if !(c.numtimes > 0) {
		return errors.New("Must specify a number greater than zero")
	}
	return nil
}

func parseArguments(args []string) (config, error) {

	var numtimes int
	var err error
	c := config{}

	if len(args) != 1 {

		return c, errors.New("Invalid number of arguments")
	}

	if args[0] == "-h" || args[0] == "--help" {
		c.printUsage = true
		return c, nil
	}

	numtimes, err = strconv.Atoi(args[0])
	if err != nil {
		return c, err
	}
	c.numtimes = numtimes
	return c, nil
}

func getName(r io.Reader, w io.Writer) (string, error) {
	msg := "Your name please ? Press the enter key when done.\n"
	fmt.Fprintf(w, msg)

	scanner := bufio.NewScanner(r)
	scanner.Scan()

	if err := scanner.Err(); err != nil {
		return "", err
	}

	name := scanner.Text()
	if len(name) == 0 {
		return "", errors.New("You did not enter your name")
	}

	return name, nil
}

func runCmd(r io.Reader, w io.Writer, c config) error {
	if c.printUsage {
		printUsage(w)
		return nil
	}

	name, err := getName(r, w)
	if err != nil {
		return err
	}

	greetUser(c, name, w)
	return nil
}

func greetUser(c config, name string, w io.Writer) {
	msg := fmt.Sprintf(" Nice to meet you %s \n", name)
	for i := 0; i < c.numtimes; i++ {
		fmt.Fprintf(w, msg)
	}
}

func main() {
	c, err := parseArguments(os.Args[1:])
	if err != nil {
		fmt.Fprintln(os.Stdout, err)
		printUsage(os.Stdout)
		os.Exit(1)
	}

	err = validateArguments(c)
	if err != nil {
		fmt.Println(os.Stdout, err)
		printUsage(os.Stdout)
		os.Exit(1)
	}

	err = runCmd(os.Stdin, os.Stdout, c)
	if err != nil {
		fmt.Println(os.Stdout, err)
		os.Exit(1)
	}
}
