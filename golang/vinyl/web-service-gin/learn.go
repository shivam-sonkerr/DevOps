package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

type areas struct {
	Location string `json:"location"`
	Weather  string `json:"weather"`
}

var area = []areas{
	{Location: "India", Weather: "Moderate"},
	{Location: "USA", Weather: "Colder"},
	{Location: "Africa", Weather: "Hot"},
}

func main() {
	r := gin.Default()
	r.GET("/area", getWeather)
	r.Run("localhost:8080")
}

func getWeather(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, area)

}
