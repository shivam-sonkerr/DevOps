package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

type friend struct {
	ID   string `json:"ID"`
	Name string `json:"Name"`
}

var friends = []friend{
	{ID: "1", Name: "Elisabeth Wilder"},
	{ID: "2", Name: "Claudia Gillespie"},
	{ID: "3", Name: "Delgado Peters"},
}

func main() {
	r := gin.Default()

	r.GET("/friends", getNames)

	r.Run("localhost:8080")
}

func getNames(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, friends)
}
