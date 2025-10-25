package main

import (
	"database/sql"
	"fmt"
	"github.com/go-sql-driver/mysql"
	"log"
)

var db *sql.DB

type Album struct {
	ID     int64
	Title  string
	Artist string
	Price  float64
}

func albumartist(name string) ([]Album, error) {

	var albums []Album

	rows, err := db.Query("SELECT * FROM album where artist =?", name)

	if err != nil {
		return nil, fmt.Errorf("albumartist %q: %v", name, err)
	}
	defer rows.Close()

	for rows.Next() {
		var alb Album
		if err := rows.Scan(&alb.ID, &alb.Title, &alb.Artist, &alb.Price); err != nil {
			return nil, fmt.Errorf("albumartist %q: %v", name, err)
		}
		albums = append(albums, alb)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("albumartist %q: %v", name, err)
	}
	return albums, nil
}

func main() {
	cfg := mysql.Config{
		User:   "root",
		Passwd: "root",
		Net:    "tcp",
		Addr:   "localhost:3306",
		DBName: "recordings",
	}
	var err error
	db, err = sql.Open("mysql", cfg.FormatDSN())
	if err != nil {
		log.Fatal(err)
	}
	pingErr := db.Ping()
	if pingErr != nil {
		log.Fatal(pingErr)
	}
	fmt.Println("Connected")

	albums, err := albumartist("John Coltrane")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Albums found: %v\n", albums)
}
