package main

import (
	"log"
	"os"

	handler "golang-api/internal/handler/telegram"
	qr "golang-api/pkg/util"

	tgbot "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func main() {
	bot, err := tgbot.NewBotAPI(os.Getenv("BOT_TOKEN"))
	if err != nil {
		log.Fatal(err)
	}

	log.Printf("Authorized as %s", bot.Self.UserName)

	qrService := qr.New(os.Getenv("PYTHON_SERVICE_URL"))
	handler := handler.New(bot, qrService)

	u := tgbot.NewUpdate(0)
	u.Timeout = 60

	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		handler.Handle(update)
	}
}
