package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"log"
)

// Album Defining the data structure type STRUCT here to hold all the values.
type Album struct {
	ID     int64
	Title  string
	Artist string
	Price  float64
}

// Function to open a database connection with all the database credentials, and using Ping functionality to check if DB is working fine.

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

//Function to get all the values of the database by writing a SQL Query and iterating over it

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

//Function to add a new value in the database and returning ID as integer value,
//note that primary key is ID and hence it is not defined as it should be unique.

func addEntry(db *sql.DB, alb Album) (int64, error) {

	query := `INSERT INTO album (Title,Artist,Price) VALUES (?,?,?)`

	result, err := db.Exec(query, alb.Title, alb.Artist, alb.Price)

	if err != nil {
		return 0, fmt.Errorf("addEntry: %v", err)
	}
	id, err := result.LastInsertId()

	if err != nil {
		return 0, fmt.Errorf("addEntry: %v", err)
	}
	return id, nil
}

func updateAlbum(db *sql.DB, alb Album) error {
	query := "UPDATE album SET title =?,artist = ?,price =?  WHERE id =?"

	result, err := db.Exec(query, alb.Title, alb.Artist, alb.Price, alb.ID)

	if err != nil {
		return fmt.Errorf("updateAlbum: %v", err)
	}

	rowsAffected, err := result.RowsAffected()

	if err != nil {
		return fmt.Errorf("updateAlbum: %v", err)
	}

	if rowsAffected == 0 {
		return fmt.Errorf("updateAlbum: no such album")
	}
	return nil
}

func deleteFromAlbum(db *sql.DB, id int) error {
	query := `DELETE FROM album WHERE id = ?`

	result, err := db.Exec(query, id)

	if err != nil {
		return fmt.Errorf("deletedFromAlbum: %v", err)
	}

	rowsAffected, err := result.RowsAffected()

	if err != nil {
		return fmt.Errorf("deletedFromAlbum: %v", err)
	}

	if rowsAffected == 0 {
		return fmt.Errorf("deleteFromAlbum: no album found with id %d", id)
	}
	return nil
}

//Main function

func main() {
	db, err := connectDB()

	if err != nil {
		log.Fatal("Failed to connect to database", err)
	}
	defer db.Close()

	fmt.Println("ALBUMS: ")

	albums, err := getArtist(db)

	if err != nil {
		log.Fatal("Failed to fetch albums", err)
	}

	//Value that will be added as part of the function addEntry into the Database.
	newAlbum := Album{
		Title:  "Linkin Park",
		Artist: "Mike",
		Price:  26,
	}

	//Adding a new value in the Database
	id, err := addEntry(db, newAlbum)

	if err != nil {
		log.Fatal("Failed to add new album: ", err)
	}
	fmt.Printf("Successfully added new album with ID: %d\n", id)

	albumtoUpdate := Album{
		ID:     1,
		Title:  "Unorthodox",
		Artist: "Bruno Mars",
		Price:  30.99,
	}

	err = updateAlbum(db, albumtoUpdate)

	if err != nil {
		fmt.Printf("Failed to update album:", err)
	}

	err = deleteFromAlbum(db, 18)
	if err != nil {
		log.Printf("Failed to Delete Album: %v", err)
	} else {
		fmt.Println("Successfully deleted album")
	}

	for _, album := range albums {
		fmt.Printf("ID: %d, Title: %s, Artist: %s, Price: %.2f\n",
			album.ID, album.Title, album.Artist, album.Price)
	}
}
