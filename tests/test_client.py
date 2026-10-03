import unittest

from unibot import Bot
from unibot.adapters.base import BaseAdapter


class FakeAdapter(BaseAdapter):
    def __init__(self, token="TOKEN"):
        super().__init__(token, "https://example.com")

    def request(self, method, data=None, files=None):
        return {"method": method, "data": data, "files": files}


class TestBot(unittest.TestCase):
    def test_custom_adapter(self):
        bot = Bot("TOKEN", provider=FakeAdapter)
        result = bot.send_message(123, "hello")
        self.assertEqual(result["method"], "sendMessage")
        self.assertEqual(result["data"]["chat_id"], 123)
        self.assertEqual(result["data"]["text"], "hello")

    def test_provider_configuration(self):
        bot = Bot("TOKEN", provider="custom", base_url="https://example.com")
        self.assertEqual(bot.adapter.base_url, "https://example.com")


if __name__ == "__main__":
    unittest.main()
