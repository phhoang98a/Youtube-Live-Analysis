package main

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	err := godotenv.Load("../.env")
	if err != nil {
		log.Fatalf("Error loading .env file")
	}

	MONGODB_URI := os.Getenv("MONGODB_URI")
	DATABASE := os.Getenv("DATABASE")
	COLLECTION := os.Getenv("COLLECTION")

	app := fiber.New()

	// Enable CORS with default settings
	app.Use(cors.New())

	clientOptions := options.Client().ApplyURI(MONGODB_URI)
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		log.Fatalf("Failed to connect to MongoDB at %v: %v", clientOptions.GetURI(), err)
	}
	log.Println("Connected to MongoDB")

	collection := client.Database(DATABASE).Collection(COLLECTION)

	app.Get("/stream", func(c *fiber.Ctx) error {
		// Set headers for Server-Sent Events (SSE)
		c.Set("Content-Type", "text/event-stream")
		c.Set("Cache-Control", "no-cache")
		c.Set("Connection", "keep-alive")

		// Use SetBodyStreamWriter with fasthttp.StreamWriter
		c.Context().SetBodyStreamWriter(func(w *bufio.Writer) {
			// Watch for changes in MongoDB collection
			changeStream, err := collection.Watch(context.Background(), mongo.Pipeline{})
			if err != nil {
				log.Printf("Failed to start MongoDB change stream: %v", err)
				return
			}
			defer changeStream.Close(context.Background())

			// Stream changes to the client
			for changeStream.Next(context.Background()) {
				var change bson.M
				if err := changeStream.Decode(&change); err != nil {
					log.Println("Error decoding MongoDB change:", err)
					continue
				}

				if change["operationType"] == "insert" {
					doc := change["fullDocument"].(bson.M)

					// Convert document to JSON and prepare SSE format
					data, err := json.Marshal(doc)
					if err != nil {
						log.Println("Error encoding JSON:", err)
						continue
					}

					// Format message for SSE
					message := fmt.Sprintf("data: %s\n\n", data)

					// Log the message
					log.Printf("Sending message to client: %s", message)

					// Write the SSE message to the client
					if _, err := w.Write([]byte(message)); err != nil {
						log.Println("Error writing to client:", err)
						return
					}

					// Flush the message to the client
					if err := w.Flush(); err != nil {
						log.Println("Error flushing to client:", err)
						return
					}
				}
			}

			if err := changeStream.Err(); err != nil {
				log.Printf("Change stream error: %v", err)
			}
		})

		return nil
	})

	log.Fatal(app.Listen(":3000"))
}
