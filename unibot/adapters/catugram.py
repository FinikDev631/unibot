from .base import BaseAdapter


class CatuGramAdapter(BaseAdapter):
    def __init__(self, token, **kwargs):
        super().__init__(
            token,
            kwargs.pop("base_url", "https://bot.catup.lol"),
            kwargs.pop("path_template", "/bot{token}/{method}"),
            kwargs.pop("timeout", 30),
        )
