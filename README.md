# UniBot

UniBot is a small provider-agnostic Python SDK for Telegram-compatible Bot APIs.

The goal is simple: write bot code once and switch the API provider without rewriting the bot logic.

## Supported providers

- Telegram
- CatuGram
- StaticGram
- Custom providers

## Installation

~~~bash
pip install git+https://github.com/FinikDev631/unibot.git
~~~

For local development:

~~~bash
git clone https://github.com/FinikDev631/unibot.git
cd unibot
pip install -e .
~~~

## Quick start

~~~python
from unibot import Bot

bot = Bot("TOKEN", provider="telegram")
print(bot.get_me())

bot.send_message(
    chat_id=123456789,
    text="Hello from UniBot!"
)
~~~

## Switching providers

~~~python
from unibot import Bot

bot = Bot("TOKEN", provider="catugram")
bot.send_message(123456789, "Hello from CatuGram!")
~~~

~~~python
from unibot import Bot

bot = Bot("TOKEN", provider="staticgram")
bot.send_message(123456789, "Hello from StaticGram!")
~~~

## Custom API

~~~python
from unibot import Bot

bot = Bot(
    "TOKEN",
    provider="custom",
    base_url="https://example.com",
    path_template="/bot{token}/{method}"
)
~~~

## Common API

~~~python
bot.get_me()
bot.get_updates()
bot.send_message(chat_id, text)
bot.send_photo(chat_id, photo, caption=None)
bot.send_document(chat_id, document, caption=None)
bot.edit_message_text(chat_id, message_id, text)
bot.delete_message(chat_id, message_id)
bot.answer_callback_query(callback_query_id, text=None)
bot.request("getChat", {"chat_id": chat_id})
~~~

Failed API responses raise BotAPIError.

## Async

~~~python
import asyncio
from unibot import AsyncBot

async def main():
    bot = AsyncBot("TOKEN", provider="telegram")
    print(await bot.get_me())
    await bot.send_message(123456789, "Hello!")

asyncio.run(main())
~~~

## Inline keyboards

~~~python
keyboard = {
    "inline_keyboard": [
        [{"text": "Open", "url": "https://example.com"}]
    ]
}

bot.send_message(123456789, "Choose:", reply_markup=keyboard)
~~~

## File uploads

~~~python
bot.send_photo(123456789, "photo.jpg", caption="Photo")
~~~

Bytes, bytearray, file objects, pathlib paths and FileUpload are supported.

## Provider configuration

The default request path is:

{base_url}/bot{token}/{method}

Both base URL and path template can be overridden.

## Design

Provider-specific transport details live in adapters. Application code uses the same Bot interface.

UniBot is dependency-free and uses Python's standard library.

## License

MIT
