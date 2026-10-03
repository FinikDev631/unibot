import asyncio

from .adapters import CatuGramAdapter, StaticGramAdapter, TelegramAdapter
from .adapters.base import BaseAdapter
from .exceptions import InvalidProviderError


PROVIDERS = {
    "telegram": TelegramAdapter,
    "catugram": CatuGramAdapter,
    "staticgram": StaticGramAdapter,
}


class Bot:
    def __init__(self, token, provider="telegram", **kwargs):
        self.token = token
        self.provider = provider.lower() if isinstance(provider, str) else provider

        if isinstance(self.provider, str) and self.provider in PROVIDERS:
            self.adapter = PROVIDERS[self.provider](token, **kwargs)
        elif self.provider == "custom":
            self.adapter = BaseAdapter(
                token,
                kwargs["base_url"],
                kwargs.get("path_template", "/bot{token}/{method}"),
                kwargs.get("timeout", 30),
            )
        elif isinstance(self.provider, type) and issubclass(self.provider, BaseAdapter):
            self.adapter = self.provider(token, **kwargs)
        else:
            raise InvalidProviderError(f"Unknown provider: {provider}")

    def request(self, method, data=None, files=None):
        return self.adapter.request(method, data, files)

    def get_me(self):
        return self.request("getMe")

    def get_updates(self, **kwargs):
        return self.request("getUpdates", kwargs)

    def send_message(self, chat_id, text, **kwargs):
        return self.request("sendMessage", {"chat_id": chat_id, "text": text, **kwargs})

    def send_photo(self, chat_id, photo, caption=None, **kwargs):
        return self.request("sendPhoto", {"chat_id": chat_id, "caption": caption, **kwargs}, {"photo": photo})

    def send_document(self, chat_id, document, caption=None, **kwargs):
        return self.request("sendDocument", {"chat_id": chat_id, "caption": caption, **kwargs}, {"document": document})

    def edit_message_text(self, chat_id, message_id, text, **kwargs):
        return self.request("editMessageText", {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            **kwargs,
        })

    def delete_message(self, chat_id, message_id):
        return self.request("deleteMessage", {"chat_id": chat_id, "message_id": message_id})

    def answer_callback_query(self, callback_query_id, text=None, **kwargs):
        return self.request("answerCallbackQuery", {
            "callback_query_id": callback_query_id,
            "text": text,
            **kwargs,
        })

    def get_chat(self, chat_id):
        return self.request("getChat", {"chat_id": chat_id})

    def get_chat_member(self, chat_id, user_id):
        return self.request("getChatMember", {"chat_id": chat_id, "user_id": user_id})


class AsyncBot:
    def __init__(self, token, provider="telegram", **kwargs):
        self._bot = Bot(token, provider, **kwargs)

    async def request(self, method, data=None, files=None):
        return await asyncio.to_thread(self._bot.request, method, data, files)

    async def get_me(self):
        return await self.request("getMe")

    async def get_updates(self, **kwargs):
        return await self.request("getUpdates", kwargs)

    async def send_message(self, chat_id, text, **kwargs):
        return await self.request("sendMessage", {"chat_id": chat_id, "text": text, **kwargs})

    async def send_photo(self, chat_id, photo, caption=None, **kwargs):
        return await self.request("sendPhoto", {"chat_id": chat_id, "caption": caption, **kwargs}, {"photo": photo})

    async def send_document(self, chat_id, document, caption=None, **kwargs):
        return await self.request("sendDocument", {"chat_id": chat_id, "caption": caption, **kwargs}, {"document": document})

    async def edit_message_text(self, chat_id, message_id, text, **kwargs):
        return await self.request("editMessageText", {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            **kwargs,
        })

    async def delete_message(self, chat_id, message_id):
        return await self.request("deleteMessage", {"chat_id": chat_id, "message_id": message_id})

    async def answer_callback_query(self, callback_query_id, text=None, **kwargs):
        return await self.request("answerCallbackQuery", {
            "callback_query_id": callback_query_id,
            "text": text,
            **kwargs,
        })

    async def get_chat(self, chat_id):
        return await self.request("getChat", {"chat_id": chat_id})

    async def get_chat_member(self, chat_id, user_id):
        return await self.request("getChatMember", {
            "chat_id": chat_id,
            "user_id": user_id,
        })
