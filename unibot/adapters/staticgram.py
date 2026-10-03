from .base import BaseAdapter


class StaticGramAdapter(BaseAdapter):
    def __init__(self, token, **kwargs):
        super().__init__(
            token,
            kwargs.pop("base_url", "https://api.staticgram.top"),
            kwargs.pop("path_template", "/bot{token}/{method}"),
            kwargs.pop("timeout", 30),
        )
