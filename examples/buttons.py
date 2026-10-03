from unibot import Bot

bot = Bot("TOKEN", provider="catugram")

keyboard = {
    "inline_keyboard": [
        [{"text": "Документация", "url": "https://github.com/FinikDev631/unibot"}]
    ]
}

bot.send_message(
    chat_id=123456789,
    text="Выбери действие:",
    reply_markup=keyboard
)
