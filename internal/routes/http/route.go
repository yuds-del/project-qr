package routes

import (
	handler "golang-api/internal/handler/http"

	"os"

	"github.com/gofiber/fiber/v2"
)

func Register(app *fiber.App) {
	baseURL := os.Getenv("QR_SERVICE_URL")
	h := handler.New(baseURL)
	api := app.Group("/api")
	api.Post("/generate-qr", h.HandleGenerateQR)
}
