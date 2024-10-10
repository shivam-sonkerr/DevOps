/*
Copyright © 2024 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// networkInfoCmd represents the networkInfo command
var networkInfoCmd = &cobra.Command{
	Use:   "networkInfo",
	Short: "A brief description of your network overall",
  Long: " ", 
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("networkInfo called")
	},
}

func init() {
	rootCmd.AddCommand(networkInfoCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// networkInfoCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// networkInfoCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
