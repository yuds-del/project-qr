package app

import (
	routes "golang-api/internal/routes/http"
	"log"
	"os"

	"github.com/gofiber/fiber/v2"
)

func HttpStart() {
	app := fiber.New()

	routes.Register(app)

	log.Fatal(app.Listen(os.Getenv("HTTP_PORT")))
}
