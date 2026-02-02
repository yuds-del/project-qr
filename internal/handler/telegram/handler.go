package handler

import (
	"strings"

	qr "golang-api/pkg/util"

	tgbot "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type Handler struct {
	Bot *tgbot.BotAPI
	QR  *qr.Service
}

func New(bot *tgbot.BotAPI, qrService *qr.Service) *Handler {
	return &Handler{
		Bot: bot,
		QR:  qrService,
	}
}

func (h *Handler) Handle(update tgbot.Update) {
	if update.Message == nil {
		return
	}

	text := update.Message.Text
	if !strings.HasPrefix(text, "/") {
		return
	}

	fields := strings.Fields(text)
	cmd := fields[0]
	args := fields[1:]

	switch cmd {
	case "/start":
		h.start(update)
	case "/qr":
		h.handleGenerateQR(update, args)
	default:
		h.reply(update, "Unknown command. Available: /qr")
	}
}

func (h *Handler) handleGenerateQR(update tgbot.Update, args []string) {
	if len(args) == 0 {
		h.reply(update, "Usage: /qr <text>")
		return
	}
	text := strings.Join(args, " ")

	data, err := h.QR.Generate(text)
	if err != nil {
		h.reply(update, err.Error())
		return
	}

	photo := tgbot.NewPhoto(
		update.Message.Chat.ID,
		tgbot.FileBytes{
			Name:  "qr.png",
			Bytes: data,
		},
	)

	h.Bot.Send(photo)
}

func (h *Handler) reply(update tgbot.Update, text string) {
	msg := tgbot.NewMessage(update.Message.Chat.ID, text)
	h.Bot.Send(msg)
}

func (h *Handler) start(update tgbot.Update) {
	msg := tgbot.NewMessage(
		update.Message.Chat.ID,
		`Saya bisa membantu kamu membuat dan mengelola layanan QR.

Gunakan perintah berikut:
/qr - Buat QR code
/help - Bantuan`,
	)
	h.Bot.Send(msg)
}
