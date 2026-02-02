// Package handler provides HTTP handlers for the QR code generation API.
//
//	@title			QR Code Generator API
//	@version		1.0
//	@description	This is a QR Code Generator API service.
//	@host			localhost:8080
//	@BasePath		/api
package handler

import (
	qr "golang-api/pkg/util"
	"log"

	"github.com/gofiber/fiber/v2"
)

type Request struct {
	Text string `json:"text"`
}

type Handler struct {
	QR *qr.Service
}

func New(baseURL string) *Handler {
	return &Handler{
		QR: qr.New(baseURL),
	}
}

func (h *Handler) HandleGenerateQR(c *fiber.Ctx) error {
	var req Request
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid Request",
		})
	}

	if req.Text == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"message": "Invalid Request",
		})
	}
	img, err := h.QR.Generate(req.Text)
	if err != nil {
		log.Fatal(err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": "Can't Generate Image",
		})
	}
	c.Set("Content-Type", "image/png")
	return c.Send(img)
}
