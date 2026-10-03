from unibot import Bot

bot = Bot("TOKEN", provider="catugram")

print(bot.get_me())

bot.send_message(
    chat_id=123456789,
    text="Привет из UniBot!"
)
