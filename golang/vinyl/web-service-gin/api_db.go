package main

import (
	"database/sql"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
	"log"
	"net/http"
)

type Album struct {
	ID     int64
	Title  string
	Artist string
	Price  float64
}

func connectDB() (*sql.DB, error) {
	db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/recordings")

	if err != nil {
		return nil, err
	}

	err = db.Ping()
	if err != nil {
		return nil, err
	}
	return db, nil
}

func getArtist(db *sql.DB) ([]Album, error) {

	var albums []Album

	query := "SELECT * from album"

	rows, err := db.Query(query)

	if err != nil {
		return nil, err
	}

	defer rows.Close()

	for rows.Next() {
		var album Album

		err := rows.Scan(&album.ID, &album.Title, &album.Artist, &album.Price)

		if err != nil {
			return nil, err
		}
		albums = append(albums, album)
	}
	return albums, err
}

func getArtistHandler(db *sql.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		albums, err := getArtist(db)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch artists"})
			return
		}
		c.IndentedJSON(http.StatusOK, albums)
	}
}

func main() {

	db, err := connectDB()

	if err != nil {
		log.Fatal("Failed to connect to database", err)
	}
	defer db.Close()

	r := gin.Default()

	r.GET("/artists", getArtistHandler(db))

	r.Run("localhost:8080")

}
